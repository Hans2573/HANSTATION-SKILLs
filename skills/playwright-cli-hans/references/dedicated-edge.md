# 启动专用 Edge

安装 Microsoft Edge 和支持 `attach --cdp` 的 `playwright-cli`。用实际的专用用户数据目录替换下面的示例目录。各任务连接同一个本机端点，并在该目录下复用用户登录。已经有对应实例在运行时，沿用它的端点。

## macOS

```bash
pw_hans_profile="$HOME/WorkTools/AgentUseEdge"
open -n -a "Microsoft Edge" --args \
  --user-data-dir="$pw_hans_profile" \
  --remote-debugging-address=127.0.0.1 \
  --remote-debugging-port=9222
```

## Windows PowerShell

```powershell
$pwHansProfile = Join-Path $env:LOCALAPPDATA 'AgentUseEdge'
$pwHansEdge = "${env:ProgramFiles(x86)}\Microsoft\Edge\Application\msedge.exe"
& $pwHansEdge "--user-data-dir=$pwHansProfile" --remote-debugging-address=127.0.0.1 --remote-debugging-port=9222
```

PowerShell 示例使用常见的 Edge 安装路径，按需替换成机器上实际的 `msedge.exe` 路径。

## 连接检查

示例的连接地址是 `http://127.0.0.1:9222`。若端口已被其他进程占用，选一个空闲端口启动专用 Edge，并让任务使用对应的地址。可在本机访问 `/json/version`，确认专用实例的 CDP 端点就绪。

如果专用目录已被未启用调试的 Edge 占用，在下次启动该实例时带上上述参数。
