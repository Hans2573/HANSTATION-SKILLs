# HANSTATION Skills

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Skills: Active](https://img.shields.io/badge/Skills-1%20Ready-success.svg)](#skills-catalog)
[![Agent: OpenCode](https://img.shields.io/badge/Agent-OpenCode-purple.svg)](https://opencode.ai)
[![Agent: Claude Code](https://img.shields.io/badge/Agent-Claude%20Code-orange.svg)](https://claude.ai)

English | [简体中文](README.md)

A curated collection of modular, production-ready AI Agent skills for OpenCode, Claude Code, Codex, and Cursor.

> [!NOTE]
> Every skill implements the standard `SKILL.md` specification with independent dependencies. Heavy sample media is isolated externally, ensuring instant loading for AI Agents.

---

## Skills Catalog

| Skill | Description | Highlights | Path | Status |
| :--- | :--- | :--- | :--- | :---: |
| [**video-transcription**](./skills/video-transcription) | Transcribes video/audio into timestamped, speaker-aligned Markdown | 100% Verbatim (No Summaries) · Fast Offline INT8 · Terminology Calibration | `skills/video-transcription` | `v0.1.0` |

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

---

## Repository Structure

```text
HANSTATION-SKILLs/
├── demos/                       # Centralized media samples (isolated from core skills)
│   └── video-transcription/
└── skills/                      # Pure skill implementations (minimal footprint)
    └── video-transcription/     # Speech-to-text & speaker alignment skill
        ├── SKILL.md             # Standard Agent contract & execution SOP
        ├── README.md            # Skill-specific documentation
        ├── pyproject.toml       # Isolated Python dependency management (uv)
        ├── config/              # Terminology calibration dictionary
        └── scripts/             # Core CLI entrypoint
```
