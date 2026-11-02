---
name: video-transcription
description: 从视频或音频文件完整提取语音内容并转录为带精准时间戳的结构化 Markdown 逐字稿文档。核心准则：专注于100%完整、无损的语音文字提取与发言人角色归属，严格禁止自行进行内容总结、概括或摘要。
keywords: [video, audio, transcribe, whisper, asr, speech-to-text, meeting, subtitles, 录音转文字, 视频提取文字, 会议逐字稿, 说话人识别, 完整记录]
---

# Video Transcription Skill (视频/音频语音提取与智能转写技能)

本技能提供从任意格式视频（`.mp4`、`.mov`、`.mkv`、`.webm` 等）或音频（`.mp3`、`.wav`、`.m4a`）中提取完整语音内容，并生成**带精准时序标记 `[mm:ss - mm:ss]`、专业术语校准、且具备多角色发言人（谁说的）结构化归属**的高质量 Markdown 逐字稿能力。

---

## ⚠️ 核心工作原则（Design Principle）

**【只做忠实提取，严禁总结/摘要】**：
* 本技能的唯一核心目标是 **100% 无损还原原始口语内容与精准时间线**。
* **严格禁止**自行对转录内容进行概括、提炼要点、生成摘要或缩减篇幅。每一句对话、每一个技术论述和每一次发问都必须被完整忠实保留，确保会议和对话记录的原貌与信息完整性。

---

## 一、 核心架构与特性

本技能采用 **“底层极速 ASR 推理 + 顶层 Agent 语义角色对齐”** 双层协同架构：

1. **无损完整转录**：严格保留全量台词与上下文细节，不做任何删减与过滤。
2. **底层隐私安全与极速转录**：完全基于本地 `faster-whisper`（CTranslate2 INT8 量化引擎），音频在本地 16kHz 无损单声道流式抽取与推理，30 分钟音频在普通 CPU 上约 2~3 分钟即可完成。
3. **专有名词与同音字校准**：内置 `config/vocabulary.json` 词典，自动纠正通用 ASR 模型常见的 IT/开发/业务同音字（如将“A型Scope”校正为“AgentScope”、“Cation声为依旧”校正为“Session升为Issue”等）。
4. **中文规范化保障**：集成 `opencc` 与提示词引导，杜绝通用 Whisper 模型因网络多语料训练而随机蹦出繁体字的问题，100% 输出标准规范简体中文。
5. **多角色发言人（谁说的）智能归属**：针对多方会议、求职面试、双人访谈等交互场景，结合参会人名单与问答逻辑上下文，自动识别并标注发言人（如 `**【张总】**`、`**【李工】**` 或 `**【面试官】**`、`**【求职者】**`）。

---

## 二、 前置依赖

1. **FFmpeg**（必须在系统 PATH 中）：
   ```bash
   brew install ffmpeg
   ```
2. **Python 环境（建议使用 `uv` 极速运行）**：
   ```bash
   uv sync
   ```

---

## 三、 执行指令 (CLI Usage)

### 1. 基础用法
在视频同级目录下自动生成 `{原文件名}_transcript.md`：
```bash
uv run scripts/transcribe.py "/path/to/your/video.mp4" -l zh
```

### 2. 常用参数
```bash
uv run scripts/transcribe.py "/path/to/your/video.mp4" \
  -o "/path/to/output.md" \
  --model base \
  --language zh \
  --threads 8
```

| 参数 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `input` | 输入视频或音频文件路径 | 必需 |
| `-o, --output` | 指定输出 Markdown 文件路径 | 自动按 `{文件名}_transcript.md` 命名 |
| `-m, --model` | Whisper 模型大小 (`tiny`, `base`, `small`, `medium`) | `base`（兼顾速度与准确度） |
| `-l, --language`| 目标语言代码 (`zh` 中文, `en` 英文) | `zh` |
| `-v, --vocab` | 业务专有名词校准字典 JSON 路径 | `config/vocabulary.json` |

---

## 四、 专有名词字典配置 (`config/vocabulary.json`)

格式为 JSON 键值对，Key 为**正确的目标词汇**，Value 为模型容易误识别的**同音字候选列表**：

```json
{
  "AgentScope": ["A型Scope", "A型scope", "a型scope"],
  "Multica": ["Mateka", "Amartica", "媒体卡"],
  "Redis": ["Release", "RIDIS"],
  "腾讯": ["统讯", "特区远"],
  "产出": ["产举"],
  "Session升为Issue": ["Cation声为依旧", "Cation声为英雄"]
}
```

---

## 五、 Agent 代理人标准操作流 (Agent Execution Protocol)

当用户在对话中提出转录需求（如：“帮我把这个会议录屏转成文字版”、“整理这个视频的逐字稿并标出谁说的”）：

### 步骤 1：执行底层 ASR 转录
调用本地命令行脚本完成高速提取：
```bash
uv run scripts/transcribe.py "<video_path>" -o "<output_markdown_path>" -l zh -m base
```

### 步骤 2：发言人识别与多角色语义归属（关键步骤）
脚本执行完成后，Agent 读取生成的原始 Markdown 文件，结合对话特征进行二次整理：
1. **识别参会人员**：
   - 若用户已在 Prompt 中提供人名（如“参会人是张三、李四”），将上下文的问询、回答、技术细节与人名精准绑定；
   - 若用户未提供明确姓名，根据对话逻辑判断角色标签（如 `【面试官】` 与 `【求职者】`，或 `【主持人】` 与 `【嘉宾】`）。
2. **合并发言流与归纳章节**：
   - 同一位发言人在同一话题下的连续短句，归入同一个发言块，格式为：  
     `**【发言人名称】** [起始时间 - 结束时间]：`
   - 按照交谈议题的转换切分章节：  
     `## 一、议题名称 [起始时间 - 结束时间]`
3. **覆写输出规范文档**：将整理后的高品质多角色逐字稿更新保存到目标 Markdown 文档中。

### 步骤 3：直接呈递完整逐字稿（严格禁止做总结与摘要）
向用户直接呈递输出的完整逐字稿文件路径与内容。**切勿自行添加任何“核心要点总结”、“会议纪要摘要”或“待办提炼”**。除非用户在后续会话中明确单独要求做总结，否则始终只交付完整无损的逐字稿。
