# HANSTATION Skills

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Skills: Active](https://img.shields.io/badge/Skills-1%20Ready-success.svg)](#技能矩阵-skills-catalog)
[![Agent: OpenCode](https://img.shields.io/badge/Agent-OpenCode-purple.svg)](https://opencode.ai)
[![Agent: Claude Code](https://img.shields.io/badge/Agent-Claude%20Code-orange.svg)](https://claude.ai)

[English](README_EN.md) | 简体中文

HANSTATION Skills 是由开发者 Hans 维护的高品质、生产级 AI 智能体（Agent）技能套件。原生适配 OpenCode、Claude Code、Codex、Cursor 等主流平台，提供开箱即用的专业能力扩展。

> [!NOTE]
> **设计哲学：模块自治与极致轻量**  
> 每一个技能均遵循标准 `SKILL.md` 契约，拥有独立的环境配置与最小运行时。媒体测试素材（如音视频 Demo）已与技能核心物理隔离存放在外层，确保 Agent 挂载与检索时零冗余、秒级响应。

---

## 技能矩阵 (Skills Catalog)

| 技能名称 | 功能说明（做什么的） | 核心亮点 | 目录入口 | 状态 |
| :--- | :--- | :--- | :--- | :---: |
| **Video Transcription**<br>`video-transcription` | **音视频完整语音提取与角色逐字稿生成**<br>从本地录像、会议录屏或音频（MP4/MOV/MP3/WAV 等）中提取全部语音，生成带精准时间戳 `[mm:ss]` 且标明**具体谁说的（如【面试官】、【求职者】或指定姓名）**的结构化 Markdown 逐字稿。 | • **100% 完整忠实还原**：契约层严格禁止模型擅自做摘要与内容缩水<br>• **语义角色归属**：结合对话逻辑推导发言人，本地 0 额外声学大模型负担<br>• **极速离线隐私**：基于 INT8 量化，默认模型仅 ~140MB，普通 CPU 2~3 分钟跑完 30 分钟音频<br>• **专有名词校准**：内置同音字词表纠偏 + OpenCC 规范简体中文 | [`skills/video-transcription`](./skills/video-transcription) | `v0.1.0` 稳定 |
| *(更多新技能持续构建中)* | 常用研发与自动化提效工作流技能 | 敬请期待... | `skills/...` | 规划中 |

---

## 快速安装与挂载

你可以根据工作习惯，选择**全量挂载**或**按需提取单技能**。

### 方式 1：按需挂载单个技能（推荐，保持工作区轻量）

以首个旗舰技能 `video-transcription` 为例：

```bash
# 挂载到 OpenCode 全局技能目录
git clone https://github.com/Hans2573/HANSTATION-SKILLs.git /tmp/HANSTATION-SKILLs
cp -r /tmp/HANSTATION-SKILLs/skills/video-transcription ~/.config/opencode/skills/
rm -rf /tmp/HANSTATION-SKILLs

# 或挂载到 Claude Code
cp -r /tmp/HANSTATION-SKILLs/skills/video-transcription ~/.claude/skills/
```

### 方式 2：克隆全量技能库

适合希望随本仓库同步更新全套技能的用户：

```bash
# 克隆至本地工具目录
git clone https://github.com/Hans2573/HANSTATION-SKILLs.git ~/HANSTATION-SKILLs

# 软链接所需技能到 Agent 技能路径
ln -s ~/HANSTATION-SKILLs/skills/video-transcription ~/.config/opencode/skills/video-transcription
```

> [!TIP]
> 每一个技能在自己的子目录中均配有独立的 `README.md` 与安装前置要求。详细使用方法请点击对应技能目录查看。

---

## 仓库架构

```text
hanstation-skills/
├── LICENSE                      # 全局 MIT 开源协议
├── README.md                    # 技能大厅中文总矩阵
├── README_EN.md                 # 技能大厅英文总矩阵
│
├── demos/                       # 集中存放所有多媒体测试样本（不污染技能核心）
│   └── video-transcription/     # 视频转写真实测试片段与 Markdown 产物
│
└── skills/                      # 纯净技能核心（专供 Agent 挂载，无冗余大文件）
    └── video-transcription/     # 视频/音频语音提取与智能转录技能
        ├── SKILL.md             # 智能体标准契约与 SOP
        ├── README.md            # 该技能专项说明文档
        ├── README_EN.md         # 该技能专项英文说明
        ├── pyproject.toml       # 独立依赖管理
        ├── config/              # 专有名词校准词库
        └── scripts/             # 核心 CLI 实现
```
