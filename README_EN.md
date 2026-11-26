# HANSTATION Skills

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Skills: Active](https://img.shields.io/badge/Skills-2%20Ready-success.svg)](#skills-catalog)
[![Agent: OpenCode](https://img.shields.io/badge/Agent-OpenCode-purple.svg)](https://opencode.ai)
[![Agent: Claude Code](https://img.shields.io/badge/Agent-Claude%20Code-orange.svg)](https://claude.ai)

English | [简体中文](README.md)

A curated collection of modular, production-ready AI Agent skills for OpenCode, Claude Code, Codex, and Cursor.

> [!NOTE]
> Each skill follows the `SKILL.md` specification and documents its runtime requirements. Sample media lives outside the skill directories.

---

## Skills Catalog

| Skill | Description | Highlights | Path | Status |
| :--- | :--- | :--- | :--- | :---: |
| [**video-transcription**](./skills/video-transcription) | Transcribes video/audio into timestamped, speaker-aligned Markdown | 100% Verbatim (No Summaries) · Fast Offline INT8 · Terminology Calibration | `skills/video-transcription` | `v0.1.0` |
| [**playwright-cli-hans**](./skills/playwright-cli-hans) | Runs parallel Playwright CLI tasks in one dedicated Edge instance | Shared sign-in · Separate CLI session per task · Manual sign-in handoff | `skills/playwright-cli-hans` | Ready |

---

## Quick Setup

### Option 1: Install Single Skill (Recommended)

```bash
# Clone temporarily and copy desired skill
git clone https://github.com/Hans2573/HANSTATION-SKILLs.git /tmp/HANSTATION-SKILLs
cp -r /tmp/HANSTATION-SKILLs/skills/video-transcription ~/.config/opencode/skills/
rm -rf /tmp/HANSTATION-SKILLs

# For Claude Code: ~/.claude/skills/
```

### Option 2: Symlink from Monorepo

```bash
git clone https://github.com/Hans2573/HANSTATION-SKILLs.git ~/HANSTATION-SKILLs
ln -s ~/HANSTATION-SKILLs/skills/video-transcription ~/.config/opencode/skills/video-transcription
```

### Playwright CLI Hans

Initialize the official Microsoft submodule bundled with the skill. It is pinned to `v0.1.24`.

```bash
git submodule update --init -- skills/playwright-cli-hans/references/upstream
```

Symlink or copy `skills/playwright-cli-hans` into your agent's skill directory. For Codex, use `~/.agents/skills/`. When copying, keep the files under `references/upstream/`. You can omit the submodule's `.git` metadata.

Choose your own dedicated Edge profile directory on first use. Relative paths resolve from your home directory, and future tasks reuse your saved choice. [First-run setup and browser launch](./skills/playwright-cli-hans/references/dedicated-edge.md)

---

## Repository Structure

```text
HANSTATION-SKILLs/
├── demos/                       # Centralized media samples (isolated from core skills)
│   └── video-transcription/
└── skills/                      # Pure skill implementations (minimal footprint)
    ├── playwright-cli-hans/     # Dedicated Edge and a CLI session per task
    │   ├── SKILL.md
    │   ├── scripts/
    │   │   └── profile-config.mjs
    │   └── references/
    │       ├── dedicated-edge.md
    │       └── upstream/        # Official Microsoft Git submodule
    └── video-transcription/     # Speech-to-text & speaker alignment skill
        ├── SKILL.md             # Standard Agent contract & execution SOP
        ├── README.md            # Skill-specific documentation
        ├── pyproject.toml       # Isolated Python dependency management (uv)
        ├── config/              # Terminology calibration dictionary
        └── scripts/             # Core CLI entrypoint
```
