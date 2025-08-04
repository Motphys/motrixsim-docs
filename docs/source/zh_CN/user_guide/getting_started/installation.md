# 🛠️ 安装 Python SDK

## 安装要求

-   **Python 版本**：{bdg-danger-line}`<3.14,>=3.10`

    | Python 版本  | 支持状态 |
    | :----------: | :------: |
    |    ≤ 3.9     |    ❌    |
    | 3.10 ～ 3.13 |    ✅    |
    |    ≥ 3.14    |    ❌    |

-   **包管理器**：{bdg-danger-line}`pip 23.0+`
    （推荐使用 [uv](https://docs.astral.sh/uv/) / [pdm](https://pdm-project.org/en/latest/) / [poetry](https://python-poetry.org/)
    等项目管理工具）

-   **系统及架构**：

    -   {bdg-danger-line}`Windows(x86_64)`
    -   {bdg-danger-line}`Linux(x86_64)`

    ```{note}
    各平台支持的功能如下：

    | 操作系统 | CPU 仿真 | 交互式查看器 | GPU 仿真 |
    | :------: | :------: | :----------: | :------: |
    |  Linux   |    ✅    |      ✅      |    🛠️ 开发中    |
    | Windows  |    ✅    |      ✅      |    🛠️ 开发中    |
    ```

## 安装方法

::::{tab-set}
:sync-group: installation-mode

:::{tab-item} 使用 pip
:sync: pip

```bash
pip install motrixsim
```

:::

:::{tab-item} 使用 uv
:sync: uv

```bash
uv add motrixsim
```

:::

:::{tab-item} 使用 pdm
:sync: pdm

```bash
pdm add motrixsim
```

:::

:::{tab-item} 使用 poetry
:sync: poetry

```bash
poetry add motrixsim
```

:::

::::

## 验证安装

::::{tab-set}
:sync-group: installation-mode

:::{tab-item} 使用 pip
:sync: pip

```bash
pip show motrixsim
```

:::

:::{tab-item} 使用 uv
:sync: uv

```bash
uv pip list | grep motrixsim
```

:::

:::{tab-item} 使用 pdm
:sync: pdm

```bash
pdm list | grep motrixsim
```

:::

:::{tab-item} 使用 poetry
:sync: poetry

```bash
poetry show | grep motrixsim
```

:::

::::
