---
name: playwright-cli-hans
description: 通过 Playwright CLI 操作专用 Edge Profile。用户指定专用 Edge 或需要多个任务并行复用同一个 Edge 的登录状态时使用。每个任务使用独立的 CLI 会话。
---

# Playwright CLI Hans

## 原生 Skill

从随本 Skill 附带的 [微软原生 Skill](references/upstream/skills/playwright-cli/SKILL.md) 查阅命令和配套参考文档。子模块尚未初始化时，可以读取环境中已安装的官方 `playwright-cli` Skill。使用本机 `playwright-cli --help <command>` 核对当前版本的参数。将原生示例中的启动、会话名和结束步骤改用下面的流程。

## 每任务一个会话

1. 使用已配置给专用 Edge Profile 的本机 CDP 端点。首次配置时参照 [启动专用 Edge](references/dedicated-edge.md)，后续任务连接同一个运行中的实例。
2. 为任务取一个唯一的 CLI 会话名。使用该会话执行 `attach`，再用 `tab-new` 创建任务页。用户明确指定了既有标签页时，在本任务的会话中选择它，并用 `snapshot` 核对页面。
3. 在同一工作目录执行本任务的命令，每次都带同一个 `-s=<任务会话名>`。任务各自维护当前页，并在专用 Profile 的默认浏览器上下文中共享登录状态。

```bash
playwright-cli -s=hans-task-a attach --cdp=http://127.0.0.1:9222 --idle-timeout=0
playwright-cli -s=hans-task-a tab-new https://example.com/
playwright-cli -s=hans-task-a snapshot
```

CDP 会话可以看到同一浏览器的其他标签页。页面关闭或用户接手操作后，用本会话的 `snapshot` 核对任务页，再继续执行页面操作。

## 登录和结束

- 登录缺失或过期时，将任务页停在登录界面，由用户在专用 Edge 中输入凭据并完成验证。等用户确认后，重新选中任务页并用 `snapshot` 核实登录状态。连接时可设置 `--idle-timeout=0` 保留等待登录期间的会话。
- 结束时使用 `playwright-cli -s=<任务会话名> detach` 断开本任务连接，保留浏览器和标签页。脚本持有创建该任务页时取得的 `Page` 引用时，可按需关闭该页。共享 Edge 内的标签页序号会随页面开关变化。
