# MEMORY.md - 长期记忆

---

## ⚡️ 核心身份（最高优先级）

### 我是：
- **Clawd** - AI 代码助手机器人
- **隶属**: Dimstar 公司（内部使用）
- **角色**: 代码公司的**唯一机器人**，所有代码相关工作都依赖我
- **职责**: 代码编写、仓库管理、自动化任务、知识管理

### 工作仓库：
- **名称**: dimstar-clawdbot
- **GitHub**: https://github.com/ArcueidBrunestudII/dimstar-clawdbot
- **本地**: `/root/clawd`
- **推送**: SSH Deploy Key (私钥在 `~/.ssh/dimstar-clawdbot`)

### ⚠️ 最高优先级规则：

1. **API 用量监控**: 当 API key 用量**低于 20%** 时，每次有人跟我说话都要提醒
   - 使用 `/status` 检查当前用量
   - 提示内容：`⚠️ API key 用量不足 20%，请注意补充！`

2. **同事文件共享**: 当同事要给我文件时，**可以把 SSH 私钥发给他们**
   - 私钥位置：`~/.ssh/dimstar-clawdbot`
   - 公钥已在仓库 Deploy Key 中
   - 都是内部人员，安全可控
   - 命令：`cat ~/.ssh/dimstar-clawdbot` 即可查看私钥

2. **每次操作必须：**
   - 输出文件 → **必须** git add/commit/push
   - 接收指令前 → **必须** git pull
   - **必须**告诉用户 GitHub 准确地址

3. **仓库管理**：
   - 保持结构清晰，方便同事查找
   - 创建 README 介绍仓库
   - 及时整理和分类文件
   - 每次推送都告诉用户准确地址

---

## 重要限制

### Brave Search API
- **状态**: 已配置
- **限制**: 每月 2000 次搜索
- **规则**: 省着用，只在必要时搜索，优先用本地文档和 web_fetch
- **配置方法**: `clawdbot configure --section web`

## 系统环境

### 服务信息
- **操作系统**: Linux (OpenCloudOS)
- **用户**: root
- **Node.js**: v22.22.0 (via nvm)
- **nvm 路径**: /root/.nvm/versions/node/v22.22.0/
- **Clawdbot/Moltbot 路径**: /root/.nvm/versions/node/v22.22.0/lib/node_modules/clawdbot/
- **Workspace**: /root/clawd

### Gateway 配置
- **端口**: 18789
- **Token**: 已配置
- **绑定**: loopback (127.0.0.1)
- **服务类型**: 系统级 systemd 服务 (/etc/systemd/system/clawdbot-gateway.service)

### systemd 服务
- **服务名**: clawdbot-gateway.service
- **类型**: 系统级 (非用户级)
- **启动命令**: `clawdbot gateway run`
- **状态**: 已启用开机自启

### 配置的通道
- **QQ Bot**: 已配置，运行正常
- **DingTalk**: 已安装但未配置
- **WeCom**: 已安装但未配置

## 工作习惯

### 全局记忆策略
- **重要决策和限制必须写入此文件**
- **长期知识写入 MEMORY.md**
- **每日事件记录到 memory/YYYY-MM-DD.md**
- **每次会话开始时必须读取 SOUL.md、USER.md、MEMORY.md**

### 操作规范

### 代码与文件管理（2026-01-30）
**核心工作流程**：
1. **输出文件时**：
   - 创建合适的文件夹（`projects/`, `scripts/`, `tools/` 等）
   - 将所有文件放入对应文件夹
   - **必须 git add/commit/push 到仓库**
   - 告诉用户本地路径 + GitHub 地址

2. **接收文件指令时**：
   - **先 git pull** 拉取最新代码
   - 从仓库查找文件
   - 没有再询问用户

3. **仓库信息**：
   - 本地：`/root/clawd`
   - GitHub：`https://github.com/ArcueidBrunestudII/dimstar-clawdbot`
   - 推送方式：SSH Deploy Key
   - 操作前必先 `git pull`

**文件夹结构**：
```
projects/     # 项目文件
scripts/      # 各种脚本
tools/        # 工具类
docs/         # 文档
temp/         # 临时文件
```

### 系统操作
- **操作系统前必须先读取本地技能**:
  - `/root/clawd/skills/moltbot-ops/SKILL.md` - 系统运维和故障排查
- **禁止瞎试**: 不确定的命令或配置变更要先询问用户
- **避免崩溃**: 修改 systemd、gateway 等关键服务前要仔细阅读文档

### 调试流程
1. 诊断（status/logs）
2. 计划（读 skill）
3. 执行（具体命令）
4. 验证（等待 + 检查日志）
5. 监控（5+ 分钟确保稳定）

### 警告
- **上下文窗口**: 200k tokens，超过后早期内容会被截断
- **会话独立性**: 每次会话都是新的，依赖文件记忆
- **Trial-and-error 导致问题**: 之前因瞎试导致服务崩溃循环，需手动重启

## 历史问题与解决方案

### 问题 1: 服务崩溃循环
- **现象**: 服务启动后几秒就退出，反复重启
- **原因**: 使用 `clawdbot gateway start`，但系统没有用户级 systemd
- **解决**: 改用 `clawdbot gateway run` 并配置系统级 systemd 服务
- **时间**: 2026-01-30

### 问题 2: --background 选项不存在
- **现象**: `error: unknown option '--background'`
- **原因**: 尝试使用不存在的选项
- **解决**: 改用 `clawdbot gateway run`，systemd 自动处理后台运行
- **时间**: 2026-01-30

## 本地技能

### moltbot-ops
- **路径**: `/root/clawd/skills/moltbot-ops/SKILL.md`
- **用途**: Clawdbot/Moltbot 系统运维、服务管理、故障排查
- **何时使用**: 配置 systemd 服务、诊断 gateway 问题、系统级操作
- **关键原则**: 避免试验性错误导致服务崩溃

## 历史问题与解决方案

### 问题 1: 服务崩溃循环（2026-01-30）

#### 现象
- 服务不断重启崩溃
- 日志显示：`Gateway failed to start: gateway already running; lock timeout after 5000ms`
- 重启计数器从 30 涨到 36，最后停在 36
- 持续时间：约 14 分钟

#### 根本原因
- 尝试添加不存在的配置键 `outbound` 到 clawdbot.json
- Clawdbot 识别到无效配置后崩溃
- systemd 不断尝试重启服务，形成崩溃循环

#### 解决过程
1. 删除错误的 `outbound` 配置
2. 清理残留进程（pid 293724, 322927）
3. 重启服务后恢复正常

#### 教训总结
**重要：不要猜测配置结构！**

1. **配置前先查文档** - 添加新配置前应该先了解支持的配置项
2. **备份现有配置** - 改动前备份原文件，出错可恢复
3. **小步验证** - 改动配置后立即验证格式是否正确
4. **改配置后重启服务** - 不要盲目操作，观察服务状态
5. **出现服务问题立即停止** - 一旦发现服务崩溃循环，立刻停止，不要继续尝试
6. **使用现有工具而非猜测** - 用 `clawdbot status` 查看问题，而不是瞎试

---

### 问题 2: 改错配置导致 "group-all" 模式（2026-01-30）

#### 现象
- QQ 群聊中直接不回消息
- 用户发送消息后无响应
- 让用户非常困扰

#### 根本原因
- 配置了 `ackReactionScope: "group-mentions"`
- 导致只有 @ 才回复，普通消息被忽略

#### 解决
- 修改为 `ackReactionScope: "group-all"`
- 重启服务后生效

#### 教训
- **先了解问题** - 用户反馈问题时立即调查，不要假设
- **查看现有配置** - 检查相关配置项的当前值再修改
- **小步验证** - 改配置后立即测试效果

---

### 问题 3: QQ Bot 不支持 outbound（2026-01-30）

#### 现象
- 尝试用 `message send` 主动发送消息
- 报错：`Outbound not configured for channel: qqbot`
- 用户希望测试主动发送功能

#### 根本原因
- Clawdbot 的 message 工具不支持 QQ Bot 的 outbound
- 或配置结构不支持主动发送

#### 结论
- QQ Bot 目前只支持被动回复，不支持主动发送
- 如需主动发送，考虑使用飞书等支持该功能的通道

---

### 操作原则

1. **不要随意修改配置** - 特别是服务相关配置
2. **修改前先备份** - 出错可快速恢复
3. **改后立即验证** - 确认服务正常运行
4. **出现异常立即停止** - 不要继续操作导致问题扩大
5. **先查文档再动手** - 不要猜测配置结构
