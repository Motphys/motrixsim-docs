# 🤖 AI Agent Skill

MotrixSim 提供一个面向 AI 编程助手（如 Claude Code、Codex 等）的 **Agent Skill**。安装后，当你让 AI 助手编写、调试或审查 MotrixSim 的 Python 程序或 MJCF XML 模型时，它会以官方版本化文档作为权威来源来确定 API 签名和 MJCF 属性，而不是凭模型记忆猜测，从而显著减少 API 名称、参数和 XML 标签上的错误。

## 安装

motrixsim skill 通过开源的 [`npx skills`](https://github.com/vercel-labs/skills) 工具分发，以 GitHub 仓库作为来源。按以下步骤安装：

1. 准备前置条件：安装 [Node.js](https://nodejs.org/en/download)（提供 `npx` 命令），并准备一个支持 Agent Skills 的 AI 编程助手（如 Claude Code 或 Codex）。

2. （可选）查看仓库内可用的 skill：

    ```bash
    npx skills add Motphys/agent-skills --list
    ```

3. 安装 motrixsim skill：

    ```bash
    npx skills add Motphys/agent-skills --skill motrixsim
    ```

```{note}
安装过程中，`npx skills` 会让你选择安装到哪个已检测到的助手；skill 会被写入对应助手的配置目录，例如 Claude Code 的 `~/.claude/skills/`、Codex 的 `~/.agents/skills/`。
```

## 使用

安装完成后无需手动调用。AI 助手会读取 skill 的描述，当你的任务匹配“编写、调试或审查 MotrixSim Python 程序或 MJCF 模型”时自动启用它。

你只需要像平常一样描述需求，例如：

-   “用 MotrixSim 写一个加载 `scene.xml` 并仿真 500 步的 Python 脚本”
-   “帮我在这个 MJCF 里加一个 hinge joint 和一个 position actuator”
-   “这段 MotrixSim 代码报错，帮我检查 API 用法”

启用后，skill 会：

1. 定位与目标版本匹配的官方文档
2. 先查阅 API / MJCF 索引，再读取具体的文档块
3. 使用文档中确切的名称和约束来生成脚本或模型
4. 在依赖可用时运行最小验证

```{note}
skill 依赖的文档来自 [Motphys/motrixsim-agent-docs](https://github.com/Motphys/motrixsim-agent-docs)，并按 MotrixSim 版本组织。如果本地缺少对应版本，skill 会从该仓库拉取匹配的标签；当确切版本不存在时，它会选择不超过目标版本的最接近版本，并提示版本差异。
```

## 相关内容

-   [安装指南](installation.md)
-   [Hello MotrixSim](hello_motrixsim.md)
-   [MJCF 参考](mjcf_reference.md)
