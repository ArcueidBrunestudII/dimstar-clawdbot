---
name: moltbot-ops
description: Clawdbot/Moltbot system operations, service management, and troubleshooting. Use when configuring systemd services, diagnosing gateway issues, or managing system-level operations to avoid trial-and-error errors that cause service crashes.
---

# Moltbot Operations Skill

## Critical: Read Before Operating

Before performing ANY system operations (systemd, service management, or gateway control), read the relevant section below. This prevents trial-and-error that causes service crashes and requires manual restarts.

## Systemd Service Management

### Understanding Service Types

Moltbot supports two systemd service types:

**User Service** (`systemctl --user`):
- Recommended for single-user setups
- Requires `loginctl enable-linger` to survive logout
- Path: `~/.config/systemd/user/moltbot-gateway[-<profile>].service`
- Does NOT work when user systemd bus is unavailable (common on some Linux distros)
- Error: `systemctl --user unavailable: Failed to connect to bus: No medium found`

**System Service** (standard `systemctl`):
- For always-on servers, multi-user environments
- Path: `/etc/systemd/system/moltbot-gateway.service`
- Survives all user sessions
- No lingering required
- Use this when user services fail

### Correct Service Configuration

**System Service Template** (recommended for servers):

```ini
[Unit]
Description=Moltbot Gateway
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/clawd
Environment="PATH=/root/.nvm/versions/node/v22.22.0/bin:/usr/local/bin:/usr/bin:/bin"
ExecStart=/root/.nvm/versions/node/v22.22.0/bin/clawdbot gateway run
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Key Points:**
- Use `clawdbot gateway run` (NOT `clawdbot gateway start`) - `start` checks for user systemd
- Set `WorkingDirectory` to workspace (default: `~/clawd` or `/root/clawd`)
- Include full PATH if using nvm
- `Restart=always` + `RestartSec=10` for auto-recovery

### Installing/Managing System Services

```bash
# Create service file (edit path as needed)
cat << 'EOF' > /etc/systemd/system/moltbot-gateway.service
[Unit]
Description=Moltbot Gateway
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/clawd
Environment="PATH=/root/.nvm/versions/node/v22.22.0/bin:/usr/local/bin:/usr/bin:/bin"
ExecStart=/root/.nvm/versions/node/v22.22.0/bin/clawdbot gateway run
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd and enable
systemctl daemon-reload
systemctl enable moltbot-gateway.service
systemctl start moltbot-gateway.service

# Check status
systemctl status moltbot-gateway.service

# View logs
journalctl -u moltbot-gateway.service -f
```

**Stopping/Restarting:**

```bash
# Stop
systemctl stop moltbot-gateway.service

# Restart
systemctl restart moltbot-gateway.service

# Disable (prevent auto-start on boot)
systemctl disable moltbot-gateway.service
```

## Gateway Operation

### Running Gateway Directly

**Foreground (for debugging):**
```bash
clawdbot gateway run --port 18789 --verbose
```

**Via systemd (recommended):**
```bash
systemctl start moltbot-gateway.service
```

**DO NOT use** `clawdbot gateway start` when:
- User systemd is unavailable (causes crash loop)
- Running under system-level systemd
- Port is 18789 (default)

The `start` subcommand checks for user systemd and fails if unavailable.

### Gateway Options

```bash
clawdbot gateway run [options]

--port <port>           # Default: 18789
--bind <mode>          # loopback|lan|tailnet|auto
--verbose               # Debug logging
--force                # Kill existing listener on port
--token <token>         # Auth token override
```

## Common Errors & Solutions

### Error 1: "systemctl --user unavailable"

```
Gateway service check failed: Error: systemctl --user unavailable: Failed to connect to bus: No medium found
```

**Cause:** Running `clawdbot gateway start` without user systemd support

**Solution:** Use `clawdbot gateway run` directly or install system service (see above)

### Error 2: "unknown option '--background'"

```
error: unknown option '--background'
```

**Cause:** Using non-existent option

**Solution:** Use `clawdbot gateway run` without --background (systemd handles background)

### Error 3: "Port 18789 is already in use"

```
Gateway failed to start: gateway already running (pid 306634)
Port 18789 is already in use.
```

**Cause:** Multiple gateway instances attempting to start

**Solution:**
```bash
# Find and kill existing instance
lsof -ti:18789 | xargs kill -9

# OR use --force flag
clawdbot gateway run --force
```

### Error 4: Service crash loop

**Symptoms:** Service exits repeatedly within seconds

**Diagnose:**
```bash
# Check recent logs
journalctl -u moltbot-gateway.service -n 50

# Look for patterns
journalctl -u moltbot-gateway.service | grep -i error
```

**Common causes:**
- Wrong `ExecStart` path
- Missing `WorkingDirectory`
- PATH not set (nvm issues)
- `clawdbot gateway start` instead of `run`

## Troubleshooting Commands

### Health Checks

```bash
# Check if gateway is running and reachable
clawdbot status

# Deep probe (includes system scans)
clawdbot status --deep

# Gateway health via RPC
clawdbot gateway status
```

### Logs

```bash
# Follow gateway logs
clawdbot logs --follow

# Systemd service logs
journalctl -u moltbot-gateway.service -f

# Last 100 lines with errors
journalctl -u moltbot-gateway.service -n 100 | grep -i error
```

### Process Management

```bash
# Find gateway processes
ps aux | grep clawdbot

# Find port listener
lsof -i:18789

# Kill specific PID
kill -9 <pid>
```

## Best Practices

### Before Making Changes

1. **Check current state:** `clawdbot status` or `systemctl status moltbot-gateway.service`
2. **Read relevant documentation:** Consult this skill or official docs
3. **Plan the change:** Know what files/commands will be affected
4. **Test in non-destructive way:** Use `--verbose` to debug before committing

### After Making Changes

1. **Verify service is stable:** Wait 30+ seconds after restart
2. **Check logs:** Ensure no errors in last 10 lines
3. **Test functionality:** Send a test message via configured channel
4. **Monitor for 5+ minutes:** Catch delayed crashes

### What NOT to Do

- ❌ Use `clawdbot gateway start` when user systemd is unavailable
- ❌ Try non-existent flags (like `--background`)
- ❌ Edit service files without `systemctl daemon-reload`
- ❌ Kill random processes - always identify the correct PID first
- ❌ Assume - verify with `clawdbot status` before declaring "fixed"

### Safe Operation Flow

```
1. Diagnose (status/logs)
   ↓
2. Plan (read this skill)
   ↓
3. Execute (specific commands only)
   ↓
4. Verify (wait + check logs)
   ↓
5. Monitor (5+ minutes for stability)
```

## Reference: Official Docs

- Gateway runbook: https://docs.molt.bot/gateway
- Systemd configuration: See "Supervision (systemd user unit)" section
- Troubleshooting: https://docs.molt.bot/channels/troubleshooting

## QQ Bot 监控与重连

**每小时检查QQ Bot连接状态：**

```bash
# 查看QQ Bot日志（最近100行）
journalctl -u clawdbot-gateway.service -n 100 | grep qqbot

# 实时监控连接状态
journalctl -u clawdbot-gateway.service -f | grep -E "(qqbot|WebSocket|closed|connected)"

# 检查会话状态
clawdbot status --deep | grep -A 20 "Sessions"
```

**关键日志关键词：**
- `WebSocket connected` - 已连接 ✅
- `WebSocket closed` - 连接断开 ❌
- `Session timed out` - 会话超时 ⚠️
- `reconnecting` - 正在重连 🔄

**重连建议：**
1. 自动重连通常在几秒到30秒内完成
2. 如果持续断开，检查网络和防火墙
3. 查看是否有 `Session timed out` 频繁出现（可能是QQ服务端问题）

**用户信息：**
- QQ号：74880657
- 群聊QQ号：249424448
- 使用 `message send --channel=qqbot --target=<QQ号> --message="内容"` 主动发送

**Remember:** This skill exists to prevent trial-and-error. Read before operating!
