# 🛠️ Environment Setup

Before running MotrixSim example programs, you need to prepare the example environment. This guide will walk you through all the steps required for environment configuration.

## Environment Setup Steps

> The following examples use the Python project management tool: [UV](https://docs.astral.sh/uv/)
>
> Please [install](https://docs.astral.sh/uv/getting-started/installation/) this tool before you begin.

### Step 1: Clone the Repository

```bash
git clone https://github.com/Motphys/motrixsim-docs
cd motrixsim-docs
git lfs pull
```

### Step 2: Install Dependencies

You can choose either of the following methods to install dependencies:

::::{tab-set}

:::{tab-item} Check for Updates and Install

```bash
uv sync --extra examples --upgrade
```

:::

:::{tab-item} Direct Install

```bash
uv sync --extra examples
```

:::

::::

### Step 4: Verify Installation

Run a simple example to verify that the environment is configured correctly:

```bash
uv run examples/empty.py
```

If the simulation window opens successfully, the environment setup is complete!

## Frequently Asked Questions

:::{card}
**Q1: Can I use something other than UV?**
^^^
A1: Absolutely! The example repository supports various Python package management tools. You just need to ensure that motrixsim and the required dependencies are installed.
:::

:::{card}
**Q2: What should I do if I encounter a model loading error when running examples?**
^^^
A2: Please make sure that:

-   The current working directory is the root of `motrixsim-docs`
-   All dependencies are correctly installed (you can check with `uv pip list`)
-   The model file paths are correct
    :::

## Next Steps

After completing the environment setup, you can:

-   See {doc}`case_comparison` for a comparison between MotrixSim and other simulators
-   Browse {doc}`examples` and {doc}`legged_gym` to explore all available examples
