# 🚀 快速入门：Hello MotrixSim

本教程将通过一个完整的实战示例 - 加载 Spot 机器狗并进行物理仿真，带你从零开始体验 MotrixSim。你将学会如何创建项目、编写代码并运行你的第一个物理仿真程序。

## 创建你的第一个 MotrixSim 项目

让我们从零开始，创建一个完整的 MotrixSim 项目。

### 步骤 1：创建项目目录

首先，创建一个新的目录来存放你的项目：

```bash
mkdir motrixsim-examples
cd motrixsim-examples
```

### 步骤 2：初始化 Python 项目

使用 `uv` 初始化一个新的 Python 项目：

```bash
uv init
```

这会创建一个基本的项目结构，包括 `pyproject.toml` 和 `.python-version` 文件。

### 步骤 3：安装 MotrixSim

使用 `uv` 安装 MotrixSim：

```bash
uv add motrixsim
```

如果你还没有安装 `uv`，可以参考 [安装指南](installation.md) 中的说明。

### 步骤 4：准备模型文件

准备一个 MJCF 格式的模型文件。你可以使用任意 MJCF 模型，如果没有，可以从我们的仓库下载示例模型：

**方法 1：下载仓库 ZIP 文件**

1. 访问 <https://github.com/Motphys/motrixsim-docs>
2. 点击绿色的 `Code` 按钮，选择 `Download ZIP`
3. 解压下载的文件
4. 将 `motrixsim-docs-main/examples/assets/boston_dynamics_spot` 文件夹复制到你的项目的 `assets/` 目录下：

```bash
# 在项目根目录下
mkdir -p assets
# 将下载解压后的 boston_dynamics_spot 文件夹复制到 assets/ 目录
```

**方法 2：使用 git 克隆**

```bash
# 克隆文档仓库（使用 --depth 1 只下载最新版本，速度更快）
git clone --depth 1 https://github.com/Motphys/motrixsim-docs.git temp-docs

# 复制模型文件到项目
mkdir -p assets
cp -r temp-docs/examples/assets/boston_dynamics_spot assets/

# 清理临时文件
rm -rf temp-docs
```

下载完成后，确保目录结构如下：

```
motrixsim-examples/
├── assets/
│   └── boston_dynamics_spot/
│       └── scene.xml
├── hello_motrixsim.py
├── pyproject.toml
└── ...
```

### 步骤 5：创建你的第一个仿真程序

创建一个名为 `hello_motrixsim.py` 的文件：

```python
# 导入 MotrixSim 库
import motrixsim as mx

# 加载模型文件（包含物理和渲染数据）
model = mx.load_model("assets/boston_dynamics_spot/scene.xml")

# 创建渲染器（"warn" 表示日志级别）
with mx.render.RenderApp("warn") as render:
    render.launch(model)          # 渲染器加载模型
    data = mx.SceneData(model)    # 创建物理数据对象
    while True:                   # 无限循环运行仿真
        model.step(data)          # 执行一步物理仿真
        render.sync(data)         # 同步数据到渲染器
```

这就是完整的代码！几行代码就完成了所有 MotrixSim 模拟实验的必需步骤。

### 步骤 6：运行你的第一个仿真

现在，运行你的程序：

**在 Linux 或 Windows 平台：**

```bash
uv run hello_motrixsim.py
```

**在 MacOS (aarch64-apple-darwin) 平台：**

```bash
uv run mxpython hello_motrixsim.py
```

```{note}
由于本示例使用了 {doc}`../main_function/render`，在 MacOS ARM64 平台上需要使用 `uv run mxpython` 来确保正确加载渲染相关的依赖和执行环境。

如果你的代码不使用 RenderApp（仅进行物理仿真计算），则使用 `uv run` 即可，与 Windows 和 Linux 平台一致。
```

### 预期结果

运行后，你应该看到类似下图的仿真窗口，Spot 四足机器人在重力作用下自然站立并保持平衡：

![hello_motrixsim](/_static/images/hello_motrixsim.png)

**恭喜！** 你已经成功运行了你的第一个 MotrixSim 仿真程序。

## 下一步

-   查看 [mjcf](mjcf.md) 已支持的功能
-   了解 [主要功能](../main_function/scene_model.md) 的使用方法
-   查看更多 [示例程序](../overview/examples.md)
