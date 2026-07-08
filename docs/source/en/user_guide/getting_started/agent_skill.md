# 🤖 AI Agent Skill

MotrixSim ships an **Agent Skill** for AI coding assistants such as Claude Code and Codex. Once installed, when you ask your assistant to write, debug, or review a MotrixSim Python program or an MJCF XML model, it resolves API signatures and MJCF attributes from the official versioned documentation instead of guessing from model memory. This greatly reduces mistakes in API names, parameters, and XML tags.

## Installation

The motrixsim skill is distributed through the open-source [`npx skills`](https://github.com/vercel-labs/skills) tool, using a GitHub repository as its source. Install it with the following steps:

1. Prepare the prerequisites: install [Node.js](https://nodejs.org/en/download) (which provides the `npx` command), and have an AI coding assistant that supports Agent Skills, such as Claude Code or Codex.

2. (Optional) List the skills available in the repository:

    ```bash
    npx skills add Motphys/agent-skills --list
    ```

3. Install the motrixsim skill:

    ```bash
    npx skills add Motphys/agent-skills --skill motrixsim
    ```

```{note}
During installation, `npx skills` lets you choose which detected assistant to install into; the skill is written to that assistant's config directory, for example `~/.claude/skills/` for Claude Code or `~/.agents/skills/` for Codex.
```

## Usage

You do not need to invoke the skill manually after installation. The assistant reads the skill description and activates it automatically when your task matches "writing, debugging, or reviewing a MotrixSim Python program or MJCF model".

Just describe what you want as usual, for example:

-   "Write a MotrixSim Python script that loads `scene.xml` and steps the simulation 500 times"
-   "Add a hinge joint and a position actuator to this MJCF for me"
-   "This MotrixSim code throws an error, check my API usage"

Once active, the skill will:

1. Locate the official docs matching the target version
2. Read the API / MJCF index first, then the specific documentation block
3. Generate the script or model using the exact names and constraints from the docs
4. Run a minimal validation when dependencies are available

```{note}
The skill relies on the documentation in [Motphys/motrixsim-agent-docs](https://github.com/Motphys/motrixsim-agent-docs), organized by MotrixSim version. If the matching version is missing locally, the skill fetches the corresponding tag from that repository; when the exact version does not exist, it picks the closest version not exceeding the target and reports the version mismatch.
```

## Related

-   [Installation](installation.md)
-   [Hello MotrixSim](hello_motrixsim.md)
-   [MJCF Reference](mjcf_reference.md)
