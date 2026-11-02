# Video Transcription Skill

English | [简体中文](README.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](../../LICENSE)
[![Python: 3.10+](https://img.shields.io/badge/python-3.10%20%7C%203.11-blue.svg)](pyproject.toml)
[![uv: supported](https://img.shields.io/badge/uv-supported-green.svg)](https://docs.astral.sh/uv/)
[![Engine: faster--whisper](https://img.shields.io/badge/Engine-faster--whisper%20(INT8)-orange.svg)](https://github.com/SYSTRAN/faster-whisper)

A lightweight, production-ready video and audio speech extraction skill for AI Agents (Claude Code, OpenCode, Codex, Cursor, OpenClaw). Transcribes recordings into structured Markdown with precise timestamps, multi-speaker role alignment, and domain vocabulary calibration—completely offline.

> [!IMPORTANT]
> **Core Principle: 100% Faithful Transcription (Strictly NO Auto-Summarization)**  
> Unlike conventional AI tools that automatically compress content or strip details, this skill is strictly bound by contract to preserve **every spoken sentence, argument, and question** without omission. It ensures zero loss of original context for meetings, interviews, legal evidence, and technical discussions.

---

## Features

- **Ultra-Lightweight & Minimal Footprint**: Eliminates the need for multi-gigabyte PyTorch installations and bulky acoustic diarization models. Powered by INT8 quantization, the default model is only **~140MB**. Speaker alignment is handled semantically by the Agent (**zero extra acoustic model overhead**), running effortlessly on standard laptop CPUs without requiring dedicated GPUs.
- **Blazing Fast & 100% Offline**: Powered by `faster-whisper` (CTranslate2 INT8 quantization). Transcribes a 30-minute recording in 2–3 minutes on a standard CPU. Audio processing is completely local—no cloud APIs required, ensuring absolute privacy for sensitive discussions.
- **Agent-Driven Speaker Alignment**: Combines millisecond-level ASR timestamps with LLM dialogue reasoning to automatically segment and assign utterances to speakers (e.g., `**【Interviewer】**`, `**【Candidate】**`, or custom participant names).
- **Domain Terminology Calibration**: Built-in `config/vocabulary.json` automatically corrects common ASR phonetic misrecognitions for IT/business terms (e.g., homophones corrected to `AgentScope`, `Redis`, `AWS`, etc.).
- **Normalized Simplified Chinese Support**: Integrated with `opencc` and prompt guidance to prevent unexpected traditional Chinese characters when processing multi-lingual speech.
- **Seamless Setup & Mirror Failover**: Effortlessly runs via modern Python tooling (`uv`) and automatically falls back to reliable mirrors (`hf-mirror.com`) for downloading and caching models without proxy hassles.

---

## Output Comparison

### Standard Whisper Output
```text
Hi Drake thanks for coming in today let's get started can you tell me about a time when you had to manage a project with a very tight deadline sure yeah so at my last job we had this big product launch and suddenly the timeline got cut by like two weeks...
```

### Video Transcription Skill Output (Timestamped & Speaker Aligned)
```markdown
## 1. Introduction and Tight Deadline Project Management [00:20 - 01:06]

**【Interviewer】** `[00:20 - 00:29]`：
- `[00:20 - 00:24]`：Hi Drake, thanks for coming in today. Let's get started.
- `[00:24 - 00:29]`：Can you tell me about a time when you had to manage a project with a very tight deadline?

**【Drake (Candidate)】** `[00:29 - 00:45]`：
- `[00:29 - 00:31]`：Sure, yeah.
- `[00:31 - 00:38]`：So at my last job, we had this big product launch, and suddenly the timeline got cut by like two weeks.
- `[00:38 - 00:41]`：The client changed their mind about the launch date.
- `[00:41 - 00:45]`：So I had to reorganize everything pretty fast.
```

---

## Project Structure

```text
skills/video-transcription/
├── README.md                    # Chinese documentation
├── README_EN.md                 # English documentation
├── SKILL.md                     # Agent skill contract specification (SOP & rules)
├── pyproject.toml               # uv / pip packaging configuration
├── uv.lock                      # Dependency lockfile
├── config/
│   └── vocabulary.json          # Domain terminology & homophone calibration dictionary
└── scripts/
    ├── transcribe.py            # Main CLI transcription entrypoint
    └── utils.py                 # Audio extraction, text normalization & formatting utilities

# Media samples are located at the repository root in demos/video-transcription/
```

---

## Prerequisites

1. **FFmpeg** (required for audio extraction):
   ```bash
   # macOS
   brew install ffmpeg

   # Ubuntu / Debian
   sudo apt update && sudo apt install -y ffmpeg

   # Windows (via Chocolatey / Scoop)
   choco install ffmpeg
   ```

2. **Python Environment**: Recommended to use [uv](https://docs.astral.sh/uv/) for instant, zero-setup execution.

---

## Quick Start

### 1. Basic CLI Usage
Transcribe any video or audio file. The Markdown result is saved alongside the input file:
```bash
uv run scripts/transcribe.py "path/to/meeting.mp4" -l en
```

### 2. Advanced Options
```bash
uv run scripts/transcribe.py "path/to/meeting.mp4" \
  -o "output/transcript.md" \
  --model base \
  --language en \
  --threads 8
```

| Parameter | Description | Default |
| :--- | :--- | :--- |
| `input` | Path to input video or audio file (`.mp4`, `.mov`, `.mp3`, etc.) | *Required* |
| `-o, --output` | Custom output Markdown file path | `{original_name}_transcript.md` |
| `-m, --model` | Whisper model size (`tiny`, `base`, `small`, `medium`) | `base` (speed & accuracy balanced) |
| `-l, --language` | Target language code (`zh`, `en`, etc.) | `zh` |
| `-v, --vocab` | Custom terminology dictionary path | `config/vocabulary.json` |
| `-t, --threads` | Number of CPU threads for inference | `8` |

---

## Using as an Agent Skill

This project natively implements the standard `SKILL.md` specification and works out-of-the-box with leading AI Agent platforms:

### Installation for Claude Code / OpenCode / Codex
Copy or symlink this skill directory into your Agent's skills folder:
```bash
# Copy method
cp -r skills/video-transcription ~/.config/opencode/skills/

# Or symlink
ln -s "$(pwd)/skills/video-transcription" ~/.claude/skills/video-transcription
```

### Agent Execution Protocol
1. **ASR Extraction**: The Agent invokes `transcribe.py` to extract raw timestamps and calibrated text locally.
2. **Speaker Identification**: The Agent inspects conversation turns and matches participants to dialog blocks according to `SKILL.md`.
3. **Delivery**: The final structured document is directly provided without intrusive summaries or bulleted compression.

---

## Customizing Vocabulary

Edit `config/vocabulary.json` to define target terms and common phonetic errors for your domain:

```json
{
  "AgentScope": ["A型Scope", "A型scope", "a型scope"],
  "Redis": ["Release", "RIDIS"],
  "Multica": ["Mateka", "Amartica"]
}
```

---

## How It Works

```text
[Media File (.mp4/.mov/.mp3/.wav)]
        │
        ▼ (FFmpeg 16kHz Mono Stream)
[faster-whisper (CTranslate2 INT8)] ──> [config/vocabulary.json & opencc normalization]
        │
        ▼ (Raw Timestamped Utterances)
[AI Agent Reasoning (SKILL.md)] ──> Contextual Speaker Assignment & Topic Segmentation
        │
        ▼
[Structured, Verbatim Markdown Document]
```
