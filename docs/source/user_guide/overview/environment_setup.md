# 🛠️ 环境准备

在运行 MotrixSim 示例程序之前，您需要准备示例环境。本指南将引导您完成环境配置的全部步骤。

## 环境配置步骤

> 以下示例使用了 Python 项目管理工具：[PDM](https://pdm-project.org/)
>
> 在开始之前，请先[安装](https://pdm-project.org/en/latest/#installation)该工具。

### 步骤 1: 克隆仓库

```bash
git clone https://github.com/Motphys/motrixsim-docs
cd motrixsim-docs
git lfs pull
```

### 步骤 2: 创建虚拟环境

```bash
pdm use 3.10
```

### 步骤 3: 安装依赖

您可以选择以下任一方式安装依赖：

::::{tab-set}

:::{tab-item} 检查更新并安装

```bash
pdm install -G examples -v
```

:::

:::{tab-item} 直接安装

```bash
pdm sync -G examples -v
```

:::

::::

### 步骤 4: 验证安装

运行一个简单的示例来验证环境配置是否成功：

```bash
pdm run examples/empty.py
```

如果能够正常打开仿真窗口，说明环境配置成功！

## 常见问题

:::{card}
**Q1: 可以不使用 PDM 吗？**
^^^
A1: 当然可以！示例仓库支持多种 Python 包管理工具。您只需要确保安装了 motrixsim 和相关依赖即可。
:::

:::{card}
**Q2: 运行示例时出现模型加载错误怎么办？**
^^^
A2: 请确保：

-   当前工作目录在 `motrixsim-docs` 根目录下
-   已正确安装所有依赖（可用 `pdm list` 检查）
-   模型文件路径正确

:::

## 下一步

环境准备完成后，您可以：

-   查看 {doc}`case_comparison` 了解 MotrixSim 与其他仿真器的对比
-   浏览 {doc}`examples` 和 {doc}`legged_gym` 了解所有可用示例
