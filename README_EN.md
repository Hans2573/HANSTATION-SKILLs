# HANSTATION Skills

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Skills: Active](https://img.shields.io/badge/Skills-1%20Ready-success.svg)](#skills-catalog)
[![Agent: OpenCode](https://img.shields.io/badge/Agent-OpenCode-purple.svg)](https://opencode.ai)
[![Agent: Claude Code](https://img.shields.io/badge/Agent-Claude%20Code-orange.svg)](https://claude.ai)

English | [简体中文](README.md)

A curated collection of modular, production-ready AI Agent skills crafted by Hans. Natively designed for OpenCode, Claude Code, Codex, and Cursor to provide robust, plug-and-play capability extensions.

> [!NOTE]
> **Design Doctrine: Modular Autonomy & Minimal Footprint**  
> Every skill strictly implements the `SKILL.md` specification with independent dependencies. Heavy sample media (such as audio/video files) are decoupled from the skills directory into an external storage structure, guaranteeing zero bloat and instant loading for AI Agents.

---

## Skills Catalog

| Skill Name | What It Does | Highlights | Path | Status |
| :--- | :--- | :--- | :--- | :---: |
| **Video Transcription**<br>`video-transcription` | **Full Speech-to-Text & Speaker-Aligned Transcript Generation**<br>Extracts speech from meeting recordings, videos, or audio files (MP4, MOV, MP3, WAV, etc.) into structured Markdown with precise timestamps `[mm:ss]` and clear **speaker attribution (e.g., `[Interviewer]`, `[Candidate]`, or designated participant names)**. | • **100% Faithful Verbatim**: Strictly bound by contract to prohibit auto-summarization or omitting content<br>• **Semantic Speaker Diarization**: Contextual role attribution with zero extra acoustic model overhead<br>• **Ultra-Fast & Offline**: Powered by INT8 quantization (~140MB model), transcribing 30 mins in 2-3 mins on CPU<br>• **Domain Terminology Calibration**: Built-in homophone correction dictionary + OpenCC Chinese normalization | [`skills/video-transcription`](./skills/video-transcription) | `v0.1.0` Ready |
| *(More skills in progress)* | Productivity & Developer workflow automation skills | Stay tuned... | `skills/...` | Planned |

---

## Installation & Setup

Choose between installing individual skills for a minimal footprint, or cloning the complete monorepo.

### Option 1: Install a Single Skill (Recommended)

Take the flagship `video-transcription` skill as an example:

```bash
# Clone temporarily and copy to OpenCode skills directory
git clone https://github.com/Hans2573/HANSTATION-SKILLs.git /tmp/HANSTATION-SKILLs
cp -r /tmp/HANSTATION-SKILLs/skills/video-transcription ~/.config/opencode/skills/
rm -rf /tmp/HANSTATION-SKILLs

# Or copy to Claude Code global directory
cp -r /tmp/HANSTATION-SKILLs/skills/video-transcription ~/.claude/skills/
```

### Option 2: Clone Complete Monorepo

Ideal for users tracking updates across all skills:

```bash
# Clone to your local workspace
git clone https://github.com/Hans2573/HANSTATION-SKILLs.git ~/HANSTATION-SKILLs

# Symlink desired skill to your Agent's skills path
ln -s ~/HANSTATION-SKILLs/skills/video-transcription ~/.config/opencode/skills/video-transcription
```

> [!TIP]
> Each individual skill includes its own dedicated `README.md` and prerequisite instructions within its folder. Click the corresponding path in the catalog above to view details.

---

## Repository Structure

```text
hanstation-skills/
├── LICENSE                      # MIT License
├── README.md                    # Monorepo Chinese overview & catalog
├── README_EN.md                 # Monorepo English overview & catalog
│
├── demos/                       # Centralized media samples (isolated from core skills)
│   └── video-transcription/     # Media samples and generated transcripts
│
└── skills/                      # Pure skill implementations (minimal footprint)
    └── video-transcription/     # Speech-to-text & speaker alignment skill
        ├── SKILL.md             # Standard Agent contract & execution SOP
        ├── README.md            # Skill-specific Chinese documentation
        ├── README_EN.md         # Skill-specific English documentation
        ├── pyproject.toml       # Isolated Python dependency management
        ├── config/              # Terminology calibration dictionary
        └── scripts/             # Core transcription CLI entrypoint
```
