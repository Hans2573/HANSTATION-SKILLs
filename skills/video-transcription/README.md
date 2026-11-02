# 视频与音频智能转写技能 (Video Transcription Skill)

[English](README_EN.md) | 简体中文

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](../../LICENSE)
[![Python: 3.10+](https://img.shields.io/badge/python-3.10%20%7C%203.11-blue.svg)](pyproject.toml)
[![uv: supported](https://img.shields.io/badge/uv-supported-green.svg)](https://docs.astral.sh/uv/)
[![Engine: faster--whisper](https://img.shields.io/badge/Engine-faster--whisper%20(INT8)-orange.svg)](https://github.com/SYSTRAN/faster-whisper)

专为 AI Agent（Claude Code、OpenCode、Codex、Cursor、OpenClaw）打造的轻量级音视频转录与逐字稿生成技能。能够将本地任意格式的音视频文件极速提取并生成带有精准时序标记 `[mm:ss - mm:ss]`、发言人角色归属、专有名词校准的高质量结构化 Markdown 逐字稿。

> [!IMPORTANT]
> **核心工作准则：100% 完整忠实还原，严格禁止擅自摘要**  
> 绝大多数 AI 工具遇到长文或视频时，都会擅自提炼要点、压缩篇幅，导致原始对话推导、论据与关键细节严重遗失。本技能在契约层**严格禁止模型自行进行内容总结、概括或缩写**，确保每一句对话、每一个技术论述和每一次发问原貌无损留存，为会议复盘、法律举证与技术分析提供坚实依据。

---

## 核心特性

- **极简轻量，告别笨重依赖**：无需安装动辄数 GB 的完整 PyTorch 与庞大声学分离大模型。基于 INT8 极限深度量化，默认模型体积仅约 **140MB**；说话人归属由顶层 Agent 语义协同完成（本地 **0 额外声学模型负担**），普通轻薄本 CPU 即可流畅飞速运行。
- **极速本地推理 & 隐私安全**：基于 `faster-whisper`（CTranslate2 INT8 引擎），音频在本地 16kHz 无损抽取与推理，30 分钟音频普通 CPU 仅需 2~3 分钟完成，数据全程不离机，完全杜绝企业与会议隐私泄露。
- **Agent 发言人智能归属（谁说的）**：将 Whisper 提取的毫秒级时间戳与大语言模型对话语义推导相结合，自动将对话切分并精准绑定至具体发言人（如 `**【面试官】**`、`**【求职者】**`，或用户指定的参会人姓名）。
- **业务专有名词校准**：内置 `config/vocabulary.json` 替换映射，自动矫正语音模型常见 IT/业务同音错别字（如将“A型Scope”自动矫正为 `AgentScope`，“特区远”矫正为 `腾讯`，“RIDIS”矫正为 `Redis`）。
- **规范简体中文**：集成 `opencc` 繁简校准与引导词机制，彻底杜绝通用 Whisper 因多语料训练随机蹦出繁体字的问题。
- **国内网络开箱即用**：自动适配国内镜像源（`hf-mirror.com`），无需科学上网即可自动高速下载并本地持久化缓存模型。

---

## 效果对比

### 通用 Whisper 原始输出
```text
主要和您介绍一下目前在特区远的工作我个人会负责一个大数据电商产品通知到一个迭代以及开发的工作好那OK你先给我介绍一下你在特区远具体做什么你有什么样的产举和价值好吗
```

### 本技能结构化输出（带时序、章节与角色归属）
```markdown
## 一、 求职者自我介绍与经历概述 [00:00 - 01:06]

**【求职者】** `[00:00 - 01:06]`：
- `[00:00 - 00:08]`：主要和您介绍一下目前在腾讯的工作。
- `[00:08 - 00:14]`：我个人会负责一个大数据电商产品通知到一个迭代以及开发的工作。

## 二、 面试官业务深入追问 [01:06 - 01:13]

**【面试官】** `[01:06 - 01:13]`：
- `[01:06 - 01:10]`：好，那OK，你先给我介绍一下，你在腾讯具体做什么？
- `[01:10 - 01:13]`：你有什么样的产出和价值，好吗？
```

---

## 目录结构

```text
skills/video-transcription/
├── README.md                    # 中文说明文档
├── README_EN.md                 # 英文说明文档
├── SKILL.md                     # Agent 技能规范契约（含角色识别 SOP 与严禁摘要指令）
├── pyproject.toml               # uv / pip 项目配置
├── uv.lock                      # 依赖版本锁定文件
├── config/
│   └── vocabulary.json          # 专有名词与同音字校准词表
└── scripts/
    ├── transcribe.py            # 核心转录命令行入口
    └── utils.py                 # 音频抽轨、繁简转换与 Markdown 生成工具

# 演示素材位于仓库根目录的 demos/video-transcription/ 中
```

---

## 环境准备

1. **安装 FFmpeg**（用于音视频高效抽轨）：
   ```bash
   # macOS
   brew install ffmpeg

   # Ubuntu / Debian
   sudo apt update && sudo apt install -y ffmpeg

   # Windows (via Chocolatey / Scoop)
   choco install ffmpeg
   ```

2. **Python 环境**：推荐使用现代 Python 包管理器 [uv](https://docs.astral.sh/uv/)，无需手动创建与管理复杂的虚拟环境。

---

## 快速上手

### 1. 基础命令行转写
直接传入音视频路径，Markdown 逐字稿将自动生成并保存在同目录下：
```bash
uv run scripts/transcribe.py "path/to/meeting.mp4" -l zh
```

### 2. 自定义参数转写
```bash
uv run scripts/transcribe.py "path/to/meeting.mp4" \
  -o "output/会议逐字稿.md" \
  --model base \
  --language zh \
  --threads 8
```

| 参数 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `input` | 输入视频或音频路径（`.mp4`, `.mov`, `.mkv`, `.webm`, `.mp3`, `.wav` 等） | *必需* |
| `-o, --output` | 指定输出 Markdown 文件路径 | `{原文件名}_transcript.md` |
| `-m, --model` | Whisper 模型规格（`tiny`, `base`, `small`, `medium`） | `base`（平衡速度与准确度） |
| `-l, --language` | 目标语言代码（`zh`, `en` 等） | `zh` |
| `-v, --vocab` | 自定义专有名词同音字词表路径 | `config/vocabulary.json` |
| `-t, --threads` | CPU 推理线程数 | `8` |

---

## 作为 AI Agent 技能使用

本项目根目录原生包含标准 `SKILL.md`，可开箱即用集成到各大 AI 平台：

### 挂载到 Claude Code / OpenCode / Codex
可将本仓库的该技能目录软链接或复制至智能体技能路径：
```bash
# 复制方式
cp -r skills/video-transcription ~/.config/opencode/skills/

# 或直接软链接
ln -s "$(pwd)/skills/video-transcription" ~/.claude/skills/video-transcription
```

### Agent 协同流程
1. **ASR 底层提取**：Agent 自动调用 `transcribe.py` 完成音频抽取与纯净带时间戳文字的转录；
2. **多角色语义对齐**：Agent 按照 `SKILL.md` 指引，根据上下文问答逻辑自动判定发言人（如求职者、面试官、各参会人员姓名）；
3. **交付完整逐字稿**：直接交付完整且对齐后的 Markdown 文档，不追加任何自行压缩的纪要或总结。

---

## 专有名词纠偏词库配置

在 `config/vocabulary.json` 中配置键值对（Key 为目标正确词汇，Value 为容易混淆的同音字词列表）：

```json
{
  "AgentScope": ["A型Scope", "A型scope", "a型scope"],
  "Redis": ["Release", "RIDIS"],
  "腾讯": ["统讯", "特区远"],
  "产出": ["产举"],
  "Session升为Issue": ["Cation声为依旧", "Cation声为英雄"]
}
```

---

## 工作原理

```text
[音视频文件 (mp4/mov/mp3/wav)]
        │
        ▼ (FFmpeg 16kHz 单声道无损抽轨)
[faster-whisper (CTranslate2 INT8 引擎)] ──> [config/vocabulary.json 词库纠偏 & opencc 规范简体]
        │
        ▼ (精准时间戳原始台词流)
[AI Agent 语义层 (SKILL.md 驱动)] ──> 上下文角色推理归属 (谁说的) + 章节划分
        │
        ▼
[结构化、100% 完整无损逐字稿 Markdown]
```
