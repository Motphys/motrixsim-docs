# 🛠️ Install Python SDK

## Installation Requirements

-   **Python Version**: {bdg-danger-line}`<3.14,>=3.10`

    | Python Version | Support Status |
    | :------------: | :------------: |
    |     ≤ 3.9      |       ❌       |
    |  3.10 ～ 3.13  |       ✅       |
    |     ≥ 3.14     |       ❌       |

-   **Package Manager**: {bdg-danger-line}`pip 23.0+`
    (It is recommended to use project management tools such
    as [uv](https://docs.astral.sh/uv/), [pdm](https://pdm-project.org/en/latest/),
    or [poetry](https://python-poetry.org/))

-   **System & Architecture**:

    -   {bdg-danger-line}`Windows(x86_64)`
    -   {bdg-danger-line}`Linux(x86_64)`
    -   {bdg-danger-line}`MacOS(aarch64)`

    ```{note}
    Supported features by platform:
    | Operating System | CPU Simulation | Interactive Viewer | GPU Simulation |
    | :--------------: | :------------: | :----------------: | :------------: |
    |      Linux       |      ✅        |        ✅          |   🛠️ In Development   |
    |     Windows      |      ✅        |        ✅          |   🛠️ In Development   |
    |      MacOS       |      ✅        |        ✅          |   🛠️ In Development   |
    ```

    ````{note}
    On MacOS (aarch64-apple-darwin) platform, when using {doc}`../main_function/render` related features, you need to use the following command format:

    ```bash
    uv run mxpython your_script.py
    ```

    This is required due to the specificity of RenderApp on MacOS ARM64 platform. Using `uv run mxpython` ensures correct loading of rendering-related dependencies and execution environment.

    **Important Notes**:
    - If your code uses {doc}`../main_function/render`, you need to use `uv run mxpython`
    - If your code **does not use** RenderApp (e.g., physics simulation only without a rendering window), use `uv run` which is consistent with Windows and Linux platforms

    ````

## Installation Methods

::::{tab-set}
:sync-group: installation-mode

:::{tab-item} Using pip
:sync: pip

```bash
pip install motrixsim
```

:::

:::{tab-item} Using uv
:sync: uv

```bash
uv add motrixsim
```

:::

:::{tab-item} Using pdm
:sync: pdm

```bash
pdm add motrixsim
```

:::

:::{tab-item} Using poetry
:sync: poetry

```bash
poetry add motrixsim
```

:::

::::

## Verify Installation

::::{tab-set}
:sync-group: installation-mode

:::{tab-item} Using pip
:sync: pip

```bash
pip show motrixsim
```

:::

:::{tab-item} Using uv
:sync: uv

```bash
uv pip list | grep motrixsim
```

:::

:::{tab-item} Using pdm
:sync: pdm

```bash
pdm list | grep motrixsim
```

:::

:::{tab-item} Using poetry
:sync: poetry

```bash
poetry show | grep motrixsim
```

:::

::::
