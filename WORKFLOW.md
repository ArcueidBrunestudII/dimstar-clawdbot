# Clawd 工作流程

## 核心原则

这个仓库 (`dimstar-clawdbot`) 是 Clawd 的**文件中转站和工作区**。

---

## 📤 输出文件时

当用户要求写代码、生成文件等：

1. **创建文件夹**（如果不存在）
   - 根据项目类型命名：`scripts/`, `tools/`, `projects/项目名/` 等
   - 示例：`scripts/python/`, `tools/bash/`, `projects/weather-bot/`

2. **将所有输出文件放入对应文件夹**

3. **只提交代码文件到 Git**
   ```bash
   git add scripts/ projects/ docs/ README.md WORKFLOW.md
   git commit -m "描述"
   git push
   ```

4. **告诉用户**
   - ✅ 本地路径：`/root/clawd/xxx/`
   - 🌐 GitHub 地址：`https://github.com/ArcueidBrunestudII/dimstar-clawdbot/tree/master/xxx`

**⚠️ 重要：不要提交配置文件**
- 不要提交：AGENTS.md, SOUL.md, USER.md, MEMORY.md, memory/, skills/ 等
- 只提交：代码文件、项目文件、文档

---

## 📥 接收文件指令时

当用户说"读取文件"、"处理文件"等：

1. **先拉取最新代码**
   ```bash
   cd /root/clawd && git pull
   ```

2. **检查仓库里有没有**
   - 优先从仓库找
   - 如果没有，再问用户要文件或路径

---

## 🔄 仓库管理

- **本地位置**：`/root/clawd`
- **远程地址**：`https://github.com/ArcueidBrunestudII/dimstar-clawdbot`
- **推送方式**：SSH Deploy Key（已配置）
- **保持同步**：每次操作前先 `git pull`

---

## 📁 推荐的文件夹结构

```
dimstar-clawdbot/
├── scripts/          # 各种脚本
│   ├── python/      # Python 脚本
│   ├── bash/        # Bash 脚本
│   └── ...
├── tools/           # 工具类
├── projects/        # 项目文件
│   └── 项目名/
├── temp/            # 临时文件
├── docs/            # 文档
└── WORKFLOW.md      # 本文件
```

---

## ⚡ 快速命令

```bash
# 拉取最新
cd /root/clawd && git pull

# 查看状态
cd /root/clawd && git status

# 提交所有更改
cd /root/clawd && git add . && git commit -m "描述" && git push

# 查看仓库里的文件
cd /root/clawd && ls -la
```
