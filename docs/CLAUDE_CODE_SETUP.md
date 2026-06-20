# CLAUDE_CODE_SETUP.md

**目的：** 在任何新机器上快速配置 Claude Code 工作环境

**适用场景：**
- 新电脑首次设置
- 多人协作（每人的电脑）
- CI/CD 环境配置

---

## 🚀 快速开始

在项目根目录执行一行命令：

```bash
bash scripts/install-hooks.sh
```

然后重启 Claude Code。完成！

---

## 📋 自动化指令（给 Agent）

将以下指令复制给 Agent，它会自动完成安装：

```
请安装 Claude Code safety hooks：

1. 执行安装脚本：
   bash scripts/install-hooks.sh

2. 报告安装结果：
   - Python 版本：[从脚本输出获取]
   - 安装状态：成功/失败
   - Rollout 模式：[从脚本输出获取]
   - 建议：重启 Claude Code 以激活 hooks

3. 注意事项：
   - 不要修改 .claude/settings.json
   - 不要修改 scripts/hooks/ 下的文件
   - 如有问题，查看 docs/HOOKS_INSTALL.md

完成后在当前 Issue 留言确认安装完成。
```

---

## 🛠️ 安装脚本做了什么

1. **检查环境**
   - 验证 Python 3 是否可用
   - 显示 Python 版本

2. **创建配置**
   - 创建 `.claude/` 目录（如果不存在）
   - 从 `scripts/hooks/claude-settings.sample.json` 提取 hooks 配置
   - 生成 `.claude/settings.json`

3. **备份保护**
   - 如果已有配置文件，先询问是否覆盖
   - 覆盖前自动备份为 `.claude/settings.json.backup`

4. **验证安装**
   - 显示生成的配置内容
   - 显示当前 rollout 模式
   - 提示下一步操作

---

## 📂 生成的配置结构

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "python3",
            "args": ["${CLAUDE_PROJECT_DIR}/scripts/hooks/pretooluse.py"]
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3",
            "args": ["${CLAUDE_PROJECT_DIR}/scripts/hooks/stop.py"]
          }
        ]
      }
    ]
  }
}
```

**Windows 用户：** 脚本会自动使用 `python` 而非 `python3`

---

## ✅ 验证安装

```bash
# 1. 检查配置文件
cat .claude/settings.json

# 2. 测试 PreToolUse hook
echo '{"tool_name":"Bash","tool_input":{"command":"echo test"}}' | python3 scripts/hooks/pretooluse.py
# 应该返回空或 audit 结果，exit code 0

# 3. 测试 Stop hook
echo '{}' | python3 scripts/hooks/stop.py
# 应该返回空或 allow 结果，exit code 0

# 4. 查看当前模式
cat scripts/hooks/config.json
# 应该显示 "rollout_mode": "audit"
```

---

## 🔄 多机部署工作流

### 场景 1：新电脑

```bash
# 1. Clone 仓库
git clone https://github.com/Baokai-and-his-agents/self-evo.git
cd self-evo/source

# 2. 安装 hooks
bash scripts/install-hooks.sh

# 3. 重启 Claude Code
# 手动重启应用程序

# 4. 验证
cat .claude/settings.json
```

---

### 场景 2：使用 Agent 自动安装

```bash
# 在新电脑上打开 Claude Code，执行：
cd self-evo/source

# 让 Agent 读取安装指令
# 方法 1：直接告诉 Agent
"请读取 docs/CLAUDE_CODE_SETUP.md 中的自动化指令部分，并执行安装。"

# 方法 2：让 Agent 自己找到文档
"这个项目需要安装 Claude Code hooks，请找到安装文档并执行。"
```

---

### 场景 3：团队协作

**第一次设置（管理员）：**
1. 在仓库 README.md 中添加链接：
   ```markdown
   ## 开发环境配置
   
   克隆仓库后，运行：
   ```bash
   bash scripts/install-hooks.sh
   ```
   
   详见 [docs/CLAUDE_CODE_SETUP.md](docs/CLAUDE_CODE_SETUP.md)
   ```

**团队成员：**
1. Clone 仓库
2. 按 README 指引运行安装脚本
3. 重启 Claude Code

---

## 🚨 故障排查

### 问题 1：`python3: command not found`

**原因：** Python 3 未安装或不在 PATH

**解决：**
- macOS: `brew install python3`
- Windows: 从 https://www.python.org/downloads/ 下载安装
- Linux: `sudo apt install python3` 或 `sudo yum install python3`

---

### 问题 2：脚本权限被拒绝

**错误：** `Permission denied: scripts/install-hooks.sh`

**解决：**
```bash
chmod +x scripts/install-hooks.sh
bash scripts/install-hooks.sh
```

---

### 问题 3：Hooks 未生效

**症状：** Agent 修改了 rules/ 但没有被记录

**检查清单：**
1. 确认 `.claude/settings.json` 存在
   ```bash
   ls -la .claude/settings.json
   ```

2. 确认内容正确
   ```bash
   cat .claude/settings.json | grep -A 5 hooks
   ```

3. **重启 Claude Code**（最重要！）
   - 完全退出应用程序
   - 重新打开
   - 在项目目录打开

4. 验证 hooks 可执行
   ```bash
   echo '{}' | python3 scripts/hooks/pretooluse.py
   echo $?  # 应该输出 0
   ```

---

### 问题 4：已有 settings.json，不想覆盖

**场景：** 你已经有自定义的 Claude Code 配置

**解决：** 手动合并

```bash
# 1. 查看现有配置
cat .claude/settings.json

# 2. 查看 hooks 配置
cat scripts/hooks/claude-settings.sample.json

# 3. 手动编辑，添加 hooks 块
nano .claude/settings.json

# 4. 确保 JSON 格式正确
python3 -m json.tool .claude/settings.json > /dev/null && echo "JSON valid"
```

---

## 🔧 高级配置

### 更改 Rollout 模式

**方法 1：环境变量（临时）**
```bash
export SELF_EVO_ROLLOUT_MODE=pretool-enforce
# 重启 Claude Code
```

**方法 2：配置文件（永久）**
```bash
# 编辑 scripts/hooks/config.json
nano scripts/hooks/config.json

# 改为：
{
  "rollout_mode": "pretool-enforce",
  "_note": "..."
}

# 重启 Claude Code
```

---

### Windows 配置

脚本会自动检测 Windows 并使用 `python` 而非 `python3`。

如果遇到问题，手动编辑 `.claude/settings.json`：

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "python",
            "args": ["${CLAUDE_PROJECT_DIR}/scripts/hooks/pretooluse.py"]
          }
        ]
      }
    ],
    "Stop": [...]
  }
}
```

---

## 📖 相关文档

- **完整文档：** `scripts/README.md`
- **安装指南：** `docs/HOOKS_INSTALL.md`
- **规则说明：** `rules/AGENT_PROTOCOL.md`
- **安全策略：** `scripts/policy.json`

---

## ❓ 常见问题

**Q: 安装后需要重启电脑吗？**
A: 不需要，只需重启 Claude Code 应用程序。

**Q: 多个项目都需要安装吗？**
A: 是的，`.claude/settings.json` 是项目级配置，每个项目独立。

**Q: 可以禁用某个 hook 吗？**
A: 可以，编辑 `.claude/settings.json`，删除对应的 hook 配置块。

**Q: Agent 能修改这个配置吗？**
A: 不能，PreToolUse hook 会拦截对 `.claude/**` 的修改。

**Q: 安装脚本是否安全？**
A: 是的，脚本只读取 `scripts/hooks/claude-settings.sample.json` 并生成配置文件，不执行任何危险操作。可以先查看脚本内容再执行。

---

## 🎯 总结

**一行命令解决所有配置：**
```bash
bash scripts/install-hooks.sh
```

**给 Agent 的指令：**
```
请读取 docs/CLAUDE_CODE_SETUP.md 中的"自动化指令（给 Agent）"部分并执行。
```

**多机部署：**
每台新电脑上执行同样的安装脚本即可。
