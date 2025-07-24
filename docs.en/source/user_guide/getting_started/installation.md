# 🛠️ Install Python SDK

## Installation Requirements

-   **Python Version**: {bdg-danger-line}`<3.14,>=3.10`

    | Python Version | Support Status |
    | :------------: | :------------: |
    |     ≤ 3.9      |      ❌        |
    |  3.10 ～ 3.13  |      ✅        |
    |     ≥ 3.14     |      ❌        |

-   **Package Manager**: {bdg-danger-line}`pip 23.0+`
    (It is recommended to use project management tools such as [uv](https://docs.astral.sh/uv/), [pdm](https://pdm-project.org/en/latest/), or [poetry](https://python-poetry.org/))

-   **System & Architecture**:

    -   {bdg-danger-line}`Windows(x86_64)`
    -   {bdg-danger-line}`Linux(x86_64)`

    ```{note}
    Supported features by platform:

    | Operating System | CPU Simulation | Interactive Viewer | GPU Simulation |
    | :--------------: | :------------: | :----------------: | :------------: |
    |      Linux       |      ✅        |        ✅          |   🛠️ In Development   |
    |     Windows      |      ✅        |        ✅          |   🛠️ In Development   |
    ```

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
