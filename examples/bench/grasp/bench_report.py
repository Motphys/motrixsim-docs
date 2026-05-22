# Copyright (C) 2020-2025 Motphys Technology Co., Ltd. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

"""Analyse grasp contact benchmark data and generate plots plus a summary report."""

import pathlib
from dataclasses import dataclass

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

PHASE_ORDER = ["move_to_lift", "move_to_grasp", "close_gripper", "lift", "settling", "hold"]

# Per-engine visual styles.  Engines are drawn in this order so that smooth
# signals (motrixsim) are rendered on top of noisy ones (mujoco).
ENGINE_STYLES = {
    "mujoco": dict(color="#5064d6", linewidth=1.5, alpha=0.86, zorder=2, linestyle="-"),
    "mujoco_fastimplicit": dict(color="#92a9f8", linewidth=1.8, alpha=0.95, zorder=7, linestyle="--"),
    "motrixsim": dict(color="#e7c7f0", linewidth=2.7, alpha=1.0, zorder=4, linestyle="-"),
}
_ENGINE_DISPLAY_NAMES = {
    "mujoco": "MuJoCo Euler",
    "mujoco_fastimplicit": "MuJoCo FastImplicit",
    "motrixsim": "Ours",
}
_DEFAULT_STYLE = dict(color="#4c566a", linewidth=1.5, alpha=0.88, zorder=2, linestyle="-")
_LIFT_ANALYSIS_WARMUP_TIME = 0.04
_FIG_DPI = 300
_RAW_DISPLAY_DOWNSAMPLE = 50
_NOISY_MAIN_EXTREMA_WINDOW = 24
_PHASE_MARKER_COLOR = "#c7cbd4"

plt.rcParams.update(
    {
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "axes.edgecolor": "black",
        "axes.linewidth": 0.8,
        "axes.labelcolor": "black",
        "axes.titlecolor": "black",
        "axes.titlesize": 13,
        "axes.titleweight": "normal",
        "axes.labelsize": 12,
        "font.family": "sans-serif",
        "font.sans-serif": ["DejaVu Sans", "Arial", "Helvetica"],
        "font.size": 11,
        "xtick.color": "black",
        "ytick.color": "black",
        "xtick.labelsize": 11,
        "ytick.labelsize": 11,
        "legend.frameon": False,
        "legend.fontsize": 11,
        "grid.color": "#c9c9c9",
        "grid.linewidth": 0.75,
        "grid.alpha": 0.95,
        "grid.linestyle": "--",
        "savefig.facecolor": "white",
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.03,
        "lines.solid_capstyle": "butt",
        "lines.dash_capstyle": "butt",
    }
)


def _engine_style(label: str) -> dict:
    """Return plot kwargs for a given engine label."""
    style = ENGINE_STYLES.get(label, _DEFAULT_STYLE).copy()
    style["label"] = _ENGINE_DISPLAY_NAMES.get(label, label)
    return style


def _sorted_engines(engines: dict[str, pd.DataFrame]) -> list[tuple[str, pd.DataFrame]]:
    """Return engines sorted so that noisy signals are drawn first (underneath)."""
    order = {k: i for i, k in enumerate(ENGINE_STYLES)}
    return sorted(engines.items(), key=lambda kv: order.get(kv[0], len(order)))


def _ordered_legend_entries(handles, labels):
    order = {"Ours": 0, "MuJoCo Euler": 1, "MuJoCo FastImplicit": 2, r"$mg$": 3}
    entries = [(handle, label) for handle, label in zip(handles, labels) if not label.startswith("_")]
    entries.sort(key=lambda entry: order.get(entry[1], len(order)))
    if not entries:
        return [], []
    ordered_handles, ordered_labels = zip(*entries)
    return list(ordered_handles), list(ordered_labels)


def _is_mujoco_engine(label: str) -> bool:
    return label.startswith("mujoco")


def _is_noisy_baseline(label: str) -> bool:
    return label == "mujoco"


def _downsample_xy(x: np.ndarray, y: np.ndarray, factor: int) -> tuple[np.ndarray, np.ndarray]:
    factor = max(1, factor)
    ids = slice(None, None, factor)
    return x[ids], y[ids]


def _window_extrema_downsample_xy(x: np.ndarray, y: np.ndarray, window: int) -> tuple[np.ndarray, np.ndarray]:
    """Downsample a dense oscillating signal while preserving each window's amplitude."""
    window = max(1, window)
    x = np.asarray(x)
    y = np.asarray(y)
    if window == 1 or len(y) <= window:
        return x, y

    selected = []
    for start in range(0, len(y), window):
        end = min(start + window, len(y))
        chunk = y[start:end]
        finite_ids = np.flatnonzero(np.isfinite(chunk))
        if finite_ids.size == 0:
            continue
        local_min = finite_ids[int(np.argmin(chunk[finite_ids]))] + start
        local_max = finite_ids[int(np.argmax(chunk[finite_ids]))] + start
        selected.extend(sorted({local_min, local_max}))

    ids = np.asarray(selected, dtype=int)
    return x[ids], y[ids]


def _detail_window(df: pd.DataFrame, focus_phases: list[str], preferred_start: float = 6.0, duration: float = 0.1):
    t_min, t_max = _phase_window(df, focus_phases)
    preferred_end = preferred_start + duration
    if preferred_end <= t_max:
        return preferred_start, preferred_end
    return max(t_min, t_max - duration), t_max


def _estimate_vertical_acceleration(df: pd.DataFrame) -> np.ndarray:
    if len(df) < 3:
        return np.zeros(len(df), dtype=float)
    t = df["time"].to_numpy(dtype=float)
    z = df["obj_z"].to_numpy(dtype=float)
    vz = np.gradient(z, t)
    return np.gradient(vz, t)


def _support_error_series(df: pd.DataFrame) -> np.ndarray:
    vf = df["vertical_friction"].to_numpy(dtype=float)
    mg = df["expected_gravity_force"].to_numpy(dtype=float)
    mass = df["object_mass"].to_numpy(dtype=float)
    phase = df["phase"].to_numpy()
    time = df["time"].to_numpy(dtype=float)
    az = _estimate_vertical_acceleration(df)

    target = np.full(len(df), np.nan, dtype=float)
    hold_mask = phase == "hold"
    lift_mask = (phase == "lift") | (phase == "settling")
    target[hold_mask] = mg[hold_mask]
    target[lift_mask] = mg[lift_mask] + mass[lift_mask] * az[lift_mask]

    err = np.full(len(df), np.nan, dtype=float)
    valid = np.isfinite(target) & (mg > 1e-8)
    err[valid] = np.abs(vf[valid] - target[valid]) / mg[valid]
    lift_time = time[phase == "lift"]
    if lift_time.size > 0:
        lift_warmup_mask = (phase == "lift") & (time < float(lift_time[0]) + _LIFT_ANALYSIS_WARMUP_TIME)
        err[lift_warmup_mask] = np.nan
    return err


def _style_axis(ax):
    ax.grid(False)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("black")
    ax.spines["bottom"].set_color("black")
    ax.tick_params(length=3.5, width=0.8, color="black")


def _panel_label(ax, label):
    ax.text(
        0.0,
        1.04,
        label,
        transform=ax.transAxes,
        fontsize=13,
        fontweight="normal",
        va="bottom",
        ha="left",
        color="black",
    )


def _save_figure(fig, path: pathlib.Path):
    fig.savefig(path, dpi=_FIG_DPI)
    plt.close(fig)


# ---------------------------------------------------------------------------
# Metric computation
# ---------------------------------------------------------------------------


@dataclass
class PhaseMetrics:
    """Summary metrics for a single phase of a single engine."""

    phase: str
    engine: str
    mean_support_error: float
    std_support_error: float
    # Object stability
    obj_z_drift_std: float  # std of obj_z (lower = more stable)
    obj_z_mean: float
    # Force smoothness (jitter = std of force derivative)
    normal_force_jitter: float
    # Contact consistency
    mean_num_contacts: float  # left + right


def compute_phase_metrics(df: pd.DataFrame, phase: str, engine: str) -> PhaseMetrics:
    pdf = df[df["phase"] == phase]
    if len(pdf) == 0:
        return PhaseMetrics(
            phase=phase,
            engine=engine,
            mean_support_error=np.nan,
            std_support_error=np.nan,
            obj_z_drift_std=np.nan,
            obj_z_mean=np.nan,
            normal_force_jitter=np.nan,
            mean_num_contacts=np.nan,
        )

    vf = pdf["vertical_friction"].values
    contacts = pdf["left_num_contacts"].values + pdf["right_num_contacts"].values
    expected_gf = float(np.mean(pdf["expected_gravity_force"].values))

    # Force jitter: std of per-step derivative of vertical friction
    if len(vf) > 1:
        force_diff = np.diff(vf)
        jitter = float(np.std(force_diff))
    else:
        jitter = 0.0

    if phase == "hold":
        mean_vf = float(np.mean(vf))
        mean_support_error = abs(mean_vf - expected_gf) / expected_gf if expected_gf > 1e-8 else np.nan
        std_support_error = float(np.std(vf) / expected_gf) if expected_gf > 1e-8 else np.nan
    elif phase in {"lift", "settling"}:
        valid_err = _support_error_series(pdf)
        valid_err = valid_err[np.isfinite(valid_err)]
        mean_support_error = float(np.mean(valid_err)) if len(valid_err) > 0 else np.nan
        std_support_error = float(np.std(valid_err)) if len(valid_err) > 0 else np.nan
    else:
        mean_support_error = np.nan
        std_support_error = np.nan

    return PhaseMetrics(
        phase=phase,
        engine=engine,
        mean_support_error=mean_support_error,
        std_support_error=std_support_error,
        obj_z_drift_std=float(np.std(pdf["obj_z"].values)),
        obj_z_mean=float(np.mean(pdf["obj_z"].values)),
        normal_force_jitter=jitter,
        mean_num_contacts=float(np.mean(contacts)),
    )


# ---------------------------------------------------------------------------
# Plotting
# ---------------------------------------------------------------------------


def _add_phase_background(ax, df):
    """Mark phase boundaries with subtle dotted lines."""
    for phase in PHASE_ORDER:
        pdf = df[df["phase"] == phase]
        if len(pdf) == 0:
            continue
        t0 = pdf["time"].iloc[0]
        if phase in {"lift", "settling", "hold"}:
            ax.axvline(t0, color=_PHASE_MARKER_COLOR, linewidth=0.8, linestyle=":", zorder=0)


def _add_phase_background_with_alpha(ax, df, alpha: float):
    """Mark phase boundaries in inset axes."""
    for phase in PHASE_ORDER:
        pdf = df[df["phase"] == phase]
        if len(pdf) == 0:
            continue
        t0 = pdf["time"].iloc[0]
        if phase in {"lift", "settling", "hold"}:
            ax.axvline(t0, color=_PHASE_MARKER_COLOR, linewidth=0.55, linestyle=":", alpha=alpha, zorder=0)


def _add_phase_header(fig, anchor_ax, df):
    """Kept for compatibility; phase labels are drawn inside axes."""
    del fig, anchor_ax, df
    return None


def _phase_window(df: pd.DataFrame, phases: list[str]) -> tuple[float, float]:
    selected = df[df["phase"].isin(phases)]
    if len(selected) == 0:
        full_t = df["time"]
        return float(full_t.iloc[0]), float(full_t.iloc[-1])
    return float(selected["time"].iloc[0]), float(selected["time"].iloc[-1])


def _phase_mask(df: pd.DataFrame, phases: list[str]) -> np.ndarray:
    return df["phase"].isin(phases).to_numpy()


def _trim_plot_edges(values: np.ndarray, trim: int) -> np.ndarray:
    trimmed = np.asarray(values, dtype=float).copy()
    if trim <= 0 or len(trimmed) <= 2 * trim:
        return trimmed
    trimmed[:trim] = np.nan
    trimmed[-trim:] = np.nan
    return trimmed


def _set_inset_ylim_from_window(
    ax,
    x: np.ndarray,
    series_list: list[np.ndarray],
    *,
    xlim: tuple[float, float],
    extra_values: list[float] | None = None,
    min_pad: float = 1e-4,
    pad_ratio: float = 0.10,
    clamp_bottom: float | None = None,
):
    x = np.asarray(x, dtype=float)
    mask = (x >= xlim[0]) & (x <= xlim[1])
    if not np.any(mask):
        return

    extrema = []
    for series in series_list:
        arr = np.asarray(series, dtype=float)
        if arr.shape != x.shape:
            continue
        window = arr[mask]
        finite = window[np.isfinite(window)]
        if finite.size > 0:
            extrema.extend([float(np.min(finite)), float(np.max(finite))])

    if extra_values:
        extrema.extend(float(v) for v in extra_values if np.isfinite(v))

    if not extrema:
        return

    lower = min(extrema)
    upper = max(extrema)
    span = upper - lower
    pad = max(min_pad, pad_ratio * span)
    y0 = lower - pad
    y1 = upper + pad
    if clamp_bottom is not None:
        y0 = max(clamp_bottom, y0)
    ax.set_ylim(y0, y1)


def _disable_axis_offset(ax):
    ax.ticklabel_format(axis="both", style="plain", useOffset=False)
    ax.xaxis.get_major_formatter().set_useOffset(False)
    ax.yaxis.get_major_formatter().set_useOffset(False)


def _force_error_stats_mn(df: pd.DataFrame, phase: str = "hold") -> tuple[float, float]:
    pdf = df[df["phase"] == phase]
    if len(pdf) == 0:
        pdf = df
    err_mn = np.abs(
        (pdf["vertical_friction"].to_numpy(dtype=float) - pdf["expected_gravity_force"].to_numpy(dtype=float)) * 1000.0
    )
    finite = err_mn[np.isfinite(err_mn)]
    if finite.size == 0:
        return np.nan, np.nan
    return float(np.mean(finite)), float(np.max(finite))


def _plot_force_error_barset(ax, engines: dict[str, pd.DataFrame]):
    bar_order = {"motrixsim": 0, "mujoco_fastimplicit": 1, "mujoco": 2}
    entries = sorted(engines.items(), key=lambda item: bar_order.get(item[0], len(bar_order)))
    labels = [_ENGINE_DISPLAY_NAMES.get(label, label) for label, _ in entries]
    means = []
    colors = []
    for label, df in entries:
        mean_err, _ = _force_error_stats_mn(df)
        means.append(max(mean_err, 1e-6))
        colors.append(ENGINE_STYLES.get(label, _DEFAULT_STYLE)["color"])

    x = np.arange(len(labels))
    ax.bar(x, means, width=0.52, color=colors, alpha=0.95)
    ax.set_yscale("log")
    mean_values = np.asarray(means, dtype=float)
    finite_values = mean_values[np.isfinite(mean_values) & (mean_values > 0.0)]
    if finite_values.size > 0:
        ax.set_ylim(float(np.min(finite_values) * 0.55), float(np.max(finite_values) * 1.9))
    ax.set_ylabel(r"Mean $|F_z-mg|$ (mN)")
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=0)
    ax.tick_params(labelsize=9)
    ax.yaxis.label.set_size(10)
    _style_axis(ax)


def plot_force_balance(engines: dict[str, pd.DataFrame], out_dir: pathlib.Path):
    """Plot 1: Vertical friction force vs expected gravity (mg) over time.

    In a horizontal grasp, the normal forces are horizontal (squeeze) and cancel out.
    The vertical component of friction forces holds the object against gravity.
    """
    fig, (ax_force, ax_bar) = plt.subplots(
        2,
        1,
        figsize=(6.8, 4.7),
        gridspec_kw={"height_ratios": [3.0, 1.35], "hspace": 0.58},
    )

    focus_phases = ["lift", "settling", "hold"]
    first_df = next(iter(engines.values()))
    t_min, t_max = _phase_window(first_df, focus_phases)
    mg = float(first_df["expected_gravity_force"].iloc[0])

    force_min = np.inf
    force_max = -np.inf

    for label, df in _sorted_engines(engines):
        t = df["time"].values
        style = _engine_style(label)
        vf = df["vertical_friction"].values
        phase_mask = _phase_mask(df, focus_phases)
        if np.any(phase_mask):
            phase_vf = vf[phase_mask]
            force_min = min(force_min, float(np.nanpercentile(phase_vf, 1)))
            force_max = max(force_max, float(np.nanpercentile(phase_vf, 99)))
        if _is_noisy_baseline(label):
            line_style = style.copy()
            line_style["linewidth"] = 0.45
            line_style["alpha"] = 0.52
            line_style["zorder"] = 2
            line_t, line_vf = _window_extrema_downsample_xy(t, vf, _NOISY_MAIN_EXTREMA_WINDOW)
            ax_force.plot(line_t, line_vf, **line_style)
        else:
            ax_force.plot(t, vf, **style)

    _add_phase_background_with_alpha(ax_force, first_df, alpha=0.34)
    ax_force.set_xlim(t_min, t_max)
    ax_force.axhline(
        mg,
        color="black",
        linestyle="--",
        linewidth=1.25,
        alpha=0.95,
        zorder=6,
        label=r"$mg$",
    )
    if np.isfinite(force_min) and np.isfinite(force_max):
        lower = min(force_min, mg)
        upper = max(force_max, mg)
        lower_pad = max(0.05, 0.20 * (upper - lower))
        upper_pad = max(0.10, 0.42 * (upper - lower))
        ax_force.set_ylim(lower - lower_pad, upper + upper_pad)

    ax_force.set_ylabel("Support force (N)")
    ax_force.set_xlabel("Time (s)")

    _style_axis(ax_force)
    _plot_force_error_barset(ax_bar, engines)

    handles, labels = _ordered_legend_entries(*ax_force.get_legend_handles_labels())
    fig.suptitle("Vertical Force Balance", y=1.04, fontsize=13, fontweight="normal")
    fig.legend(
        handles,
        labels,
        loc="upper center",
        bbox_to_anchor=(0.5, 0.985),
        ncol=min(4, len(labels)),
        columnspacing=1.2,
        handlelength=2.0,
    )
    fig.subplots_adjust(top=0.76)
    _save_figure(fig, out_dir / "force_balance.png")


def _hold_jitter(df: pd.DataFrame, column: str) -> float:
    """Compute jitter (std of per-step difference) for *column* during hold phase."""
    hold = df[df["phase"] == "hold"]
    if len(hold) < 2:
        return np.nan
    values = hold[column].to_numpy(dtype=float)
    return float(np.std(np.diff(values)))


def plot_force_smoothness(engines: dict[str, pd.DataFrame], out_dir: pathlib.Path):
    """Grouped bar chart comparing hold-phase Fz and Fn jitter across engines."""
    bar_order = {"motrixsim": 0, "mujoco_fastimplicit": 1, "mujoco": 2}
    entries = sorted(engines.items(), key=lambda item: bar_order.get(item[0], len(bar_order)))
    labels = [_ENGINE_DISPLAY_NAMES.get(label, label) for label, _ in entries]
    jitters_fz = []
    jitters_fn = []
    colors = []
    for label, df in entries:
        jitters_fz.append(max(_hold_jitter(df, "vertical_friction"), 1e-8))
        jitters_fn.append(max(_hold_jitter(df, "total_normal_force"), 1e-8))
        colors.append(ENGINE_STYLES.get(label, _DEFAULT_STYLE)["color"])

    fig, ax = plt.subplots(figsize=(5.6, 3.4))
    x = np.arange(len(labels))
    bar_width = 0.32
    ax.bar(x - bar_width / 2, jitters_fz, width=bar_width, color=colors, alpha=0.95, label=r"$\Delta F_z$")
    ax.bar(x + bar_width / 2, jitters_fn, width=bar_width, color=colors, alpha=0.55, label=r"$\Delta F_n$")
    ax.set_yscale("log")
    all_values = np.asarray(jitters_fz + jitters_fn, dtype=float)
    finite_values = all_values[np.isfinite(all_values) & (all_values > 0.0)]
    if finite_values.size > 0:
        ax.set_ylim(float(np.min(finite_values) * 0.55), float(np.max(finite_values) * 1.9))
    ax.set_ylabel("Jitter  std (N)")
    ax.set_title("Contact Force Smoothness (hold phase)")
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=0)
    ax.legend(loc="upper left")
    _style_axis(ax)
    fig.tight_layout()
    _save_figure(fig, out_dir / "force_smoothness.png")


# ---------------------------------------------------------------------------
# Summary report
# ---------------------------------------------------------------------------


def generate_report(
    all_metrics: list[PhaseMetrics],
    engines: dict[str, pd.DataFrame],
    out_dir: pathlib.Path,
    run_summaries: list[dict] | None = None,
):
    lines = []
    engine_width = 20
    lines.append("=" * 80)
    lines.append("GRASP CONTACT BENCHMARK — COMPARISON REPORT")
    lines.append("=" * 80)

    # ── Field descriptions ──
    lines.append("")
    lines.append("Field descriptions:")
    lines.append("  Engine      - Physics engine (and integrator variant) used for this run.")
    lines.append("  dt(s)       - Simulation timestep in seconds.")
    lines.append("  Mass(kg)    - Object mass in kilograms.")
    lines.append("  mg(N)       - Object weight (mass * gravity magnitude) in newtons.")
    lines.append("  Duration(s) - Total simulated time in seconds.")
    lines.append("  FinalZ(m)   - Object height at the end of simulation in meters.")
    lines.append("  Held        - Whether the object stayed above the drop threshold.")
    lines.append("  GravErr%    - Mean |Fz - mg| / mg during hold phase (lower = better).")
    lines.append("  DynErr%     - Mean |Fz - (mg + m*az)| / mg during lift/settling (lower = better).")
    lines.append("  Z_std(mm)   - Std of object height in millimeters (lower = more stable).")
    lines.append("  Jitter      - Std of per-step vertical friction force difference (lower = smoother).")
    lines.append("  Contacts    - Mean number of active contact points (left + right fingers).")

    # ── Simulation overview ──
    if run_summaries:
        lines.append(f"\n{'─' * 40}")
        lines.append("Simulation Overview")
        lines.append(f"{'─' * 40}")
        columns = [
            ("engine", "Engine", 20),
            ("dt", "dt(s)", 8),
            ("mass", "Mass(kg)", 10),
            ("expected_gf", "mg(N)", 8),
            ("total_duration", "Duration(s)", 12),
            ("final_z", "FinalZ(m)", 10),
            ("held", "Held", 6),
        ]
        header = " ".join(title.ljust(width) for _, title, width in columns)
        lines.append(header)
        lines.append("-" * len(header))
        for row in run_summaries:
            values = []
            for key, _, width in columns:
                value = row.get(key)
                if key == "held":
                    text = "YES" if value else "NO"
                elif isinstance(value, float):
                    text = f"{value:.4f}"
                else:
                    text = str(value) if value is not None else "-"
                values.append(text.ljust(width))
            lines.append(" ".join(values))

    # ── Per-phase metrics ──
    for phase in ["close_gripper", "lift", "settling", "hold"]:
        lines.append(f"\n{'─' * 40}")
        lines.append(f"Phase: {phase.upper()}")
        lines.append(f"{'─' * 40}")

        phase_metrics = [m for m in all_metrics if m.phase == phase]
        if not phase_metrics:
            lines.append("  (no data)")
            continue

        if phase == "close_gripper":
            header = f"{'Engine':<{engine_width}} {'Jitter':>10} {'Contacts':>10}"
        elif phase in {"lift", "settling"}:
            header = f"{'Engine':<{engine_width}} {'DynErr%':>10} {'Jitter':>10} {'Contacts':>10}"
        else:
            header = f"{'Engine':<{engine_width}} {'GravErr%':>10} {'Z_std(mm)':>10} {'Jitter':>10} {'Contacts':>10}"
        lines.append(header)
        lines.append("-" * len(header))

        for m in phase_metrics:
            if phase == "close_gripper":
                lines.append(f"{m.engine:<{engine_width}} {m.normal_force_jitter:>10.4f} {m.mean_num_contacts:>10.1f}")
            elif phase in {"lift", "settling"}:
                lines.append(
                    f"{m.engine:<{engine_width}} "
                    f"{m.mean_support_error * 100:>9.2f}% "
                    f"{m.normal_force_jitter:>10.4f} "
                    f"{m.mean_num_contacts:>10.1f}"
                )
            else:
                lines.append(
                    f"{m.engine:<{engine_width}} "
                    f"{m.mean_support_error * 100:>9.2f}% "
                    f"{m.obj_z_drift_std * 1000:>9.3f} "
                    f"{m.normal_force_jitter:>10.4f} "
                    f"{m.mean_num_contacts:>10.1f}"
                )

    lines.append("")

    report = "\n".join(lines)
    print(report)
    print(f"\nPlots saved to {out_dir}/")
    return report


def analyze_engines(
    engines: dict[str, pd.DataFrame],
    out_dir: pathlib.Path,
    run_summaries: list[dict] | None = None,
):
    out_dir.mkdir(parents=True, exist_ok=True)

    all_metrics = []
    for label, df in engines.items():
        for phase in PHASE_ORDER:
            m = compute_phase_metrics(df, phase, label)
            all_metrics.append(m)

    plot_force_balance(engines, out_dir)
    plot_force_smoothness(engines, out_dir)

    return generate_report(all_metrics, engines, out_dir, run_summaries)
