# 首次设置与启动专用 Edge

安装 Microsoft Edge 和支持 `attach --cdp` 的 `playwright-cli`。首次使用时，为自动化选择一个独立的 Edge 用户数据目录。配置保存在自己的 `~/.playwright-cli-hans/edge.json`，该目录下的同一份配置可供不同项目复用。

## 选择 Profile 目录

以下示例使用 Codex 的全局安装路径。使用其他安装位置时，将脚本路径换成实际路径。

```bash
node "$HOME/.agents/skills/playwright-cli-hans/scripts/profile-config.mjs" setup "WorkTools/Agent Edge"
```

支持绝对路径、`~/` 路径和普通相对路径。普通相对路径从用户主目录解析。例如 `WorkTools/Agent Edge` 会解析到该用户主目录下的 `WorkTools/Agent Edge`。首次运行 `setup` 时省略目录可选用 `~/.playwright-cli-hans/edge-profile`。Edge 会在首次启动时创建数据目录。已有专用目录时，可以选回该目录并沿用登录状态。

`setup` 会保存选择，末尾可追加端口，初始默认值为 `9222`。再次运行 `setup` 时，省略的值沿用已保存的设置。`get` 会返回解析后的 `profileDir`、`cdpPort` 和 `cdpEndpoint`。

## 启动与复用

已经有对应实例在运行时，沿用其端点。首次启动时执行下面对应系统的命令。

### macOS

```bash
if pw_hans_config="$(node "$HOME/.agents/skills/playwright-cli-hans/scripts/profile-config.mjs" get)"; then
  pw_hans_profile="$(node -p 'JSON.parse(process.argv[1]).profileDir' "$pw_hans_config")"
  pw_hans_port="$(node -p 'JSON.parse(process.argv[1]).cdpPort' "$pw_hans_config")"
  open -n -a "Microsoft Edge" --args \
    --user-data-dir="$pw_hans_profile" \
    --remote-debugging-address=127.0.0.1 \
    --remote-debugging-port="$pw_hans_port"
fi
```

### Windows PowerShell

```powershell
$pwHansConfig = node "$HOME/.agents/skills/playwright-cli-hans/scripts/profile-config.mjs" get
if ($LASTEXITCODE -eq 0) {
    $pwHansSettings = $pwHansConfig | ConvertFrom-Json
    $pwHansEdge = "${env:ProgramFiles(x86)}\Microsoft\Edge\Application\msedge.exe"
    & $pwHansEdge "--user-data-dir=$($pwHansSettings.profileDir)" `
        --remote-debugging-address=127.0.0.1 "--remote-debugging-port=$($pwHansSettings.cdpPort)"
}
```

PowerShell 示例使用常见的 Edge 安装路径，按需替换成机器上实际的 `msedge.exe` 路径。

## 连接检查

任务使用 `get` 返回的 `cdpEndpoint` 连接。如果端口已被其他进程占用，选一个空闲端口，用 `setup` 保存目录和新端口。可在已配置的端点上访问 `/json/version`，确认专用实例可连接。

变更目录或端口后，下次启动专用 Edge 时使用新设置。连接前确认该端点对应所选目录的实例。如果专用目录已被未启用调试的 Edge 占用，在下次启动该实例时带上上述参数。
