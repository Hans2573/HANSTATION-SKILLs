# HANSTATION Skills

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Skills: Active](https://img.shields.io/badge/Skills-2%20Ready-success.svg)](#技能矩阵)
[![Agent: OpenCode](https://img.shields.io/badge/Agent-OpenCode-purple.svg)](https://opencode.ai)
[![Agent: Claude Code](https://img.shields.io/badge/Agent-Claude%20Code-orange.svg)](https://claude.ai)

[English](README_EN.md) | 简体中文

面向现代 AI 智能体（OpenCode, Claude Code, Codex, Cursor）的高品质模块化技能套件。

> [!NOTE]
> 每个技能遵循 `SKILL.md` 规范，并说明所需的运行环境。测试样本放在技能目录之外。

---

## 技能矩阵

| 技能 | 功能简介 | 核心亮点 | 路径 | 状态 |
| :--- | :--- | :--- | :--- | :---: |
| [**video-transcription**](./skills/video-transcription) | 音视频极速转写为带时间戳与发言人归属的结构化 Markdown 逐字稿 | 100% 忠实还原（严禁摘要） · 离线 INT8 极速推理 · 专有名词校准 | `skills/video-transcription` | `v0.1.0` |
| [**playwright-cli-hans**](./skills/playwright-cli-hans) | 在同一个专用 Edge 中并行执行 Playwright CLI 任务 | 复用登录态 · 每任务独立会话 · 人工登录交接 | `skills/playwright-cli-hans` | 可用 |

---

## 快速挂载

### 方式 1：按需挂载单个技能（推荐）

```bash
# 以 video-transcription 为例，直接复制到智能体技能目录
git clone https://github.com/Hans2573/HANSTATION-SKILLs.git /tmp/HANSTATION-SKILLs
cp -r /tmp/HANSTATION-SKILLs/skills/video-transcription ~/.config/opencode/skills/
rm -rf /tmp/HANSTATION-SKILLs

# Claude Code 目录：~/.claude/skills/
```

### 方式 2：全量软链接

```bash
git clone https://github.com/Hans2573/HANSTATION-SKILLs.git ~/HANSTATION-SKILLs
ln -s ~/HANSTATION-SKILLs/skills/video-transcription ~/.config/opencode/skills/video-transcription
```

### Playwright CLI Hans

在仓库中初始化随 Skill 附带的微软官方子模块，版本固定在 `v0.1.24`。

```bash
git submodule update --init -- skills/playwright-cli-hans/references/upstream
```

将 `skills/playwright-cli-hans` 软链接或复制到智能体的技能目录。Codex 使用 `~/.agents/skills/`。复制时保留 `references/upstream/` 里的文件，子模块的 `.git` 元数据可以省略。

连接共享 Edge 前，参照 [专用 Edge 启动说明](./skills/playwright-cli-hans/references/dedicated-edge.md) 配置一次本机 CDP 端点。

---

## 目录结构

```text
HANSTATION-SKILLs/
├── demos/                       # 多媒体演示素材（与技能核心物理隔离）
│   └── video-transcription/
└── skills/                      # 纯净技能核心（供 Agent 挂载，零冗余）
    ├── playwright-cli-hans/     # 专用 Edge 与每任务独立 CLI 会话
    │   ├── SKILL.md
    │   └── references/
    │       ├── dedicated-edge.md
    │       └── upstream/        # 微软官方 Git 子模块
    └── video-transcription/     # 视频/音频语音提取与智能转写
        ├── SKILL.md             # 智能体标准契约与 SOP
        ├── README.md            # 技能专属详细说明
        ├── pyproject.toml       # 独立依赖管理 (uv)
        ├── config/              # 专有名词纠偏词库
        └── scripts/             # 核心 CLI 入口
```
