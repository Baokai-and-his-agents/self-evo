# Hooks 快速安装指南

## 一行命令安装

在项目根目录执行：

```bash
bash scripts/install-hooks.sh
```

这将自动：
1. 检查 Python 3 环境
2. 创建 `.claude/settings.json`
3. 安装 PreToolUse 和 Stop hooks
4. 设置为 audit 模式（只记录不阻止）

## 给 Agent 的自动化提示词

```
请执行以下步骤安装 Claude Code safety hooks：

1. 运行安装脚本：
   bash scripts/install-hooks.sh

2. 确认安装成功后，在 Issue comment 中报告：
   - Python 版本
   - 安装状态（成功/失败）
   - 当前 rollout 模式

3. 不要修改 .claude/settings.json 的内容
```

## 手动安装（如果脚本失败）

1. 确保 Python 3 已安装：`python3 --version`
2. 创建目录：`mkdir -p .claude`
3. 复制配置：
   ```bash
   python3 -c "import json; s=json.load(open('scripts/hooks/claude-settings.sample.json')); json.dump({'hooks':s['hooks']}, open('.claude/settings.json','w'), indent=2)"
   ```
4. 重启 Claude Code

## 验证安装

```bash
# 检查配置文件是否存在
cat .claude/settings.json

# 测试 PreToolUse hook
echo '{}' | python3 scripts/hooks/pretooluse.py

# 测试 Stop hook
echo '{}' | python3 scripts/hooks/stop.py
```

## 多机部署

在每台新电脑上：
1. Clone 仓库
2. 运行 `bash scripts/install-hooks.sh`
3. 重启 Claude Code

## 卸载

删除 `.claude/settings.json` 并重启 Claude Code。

## 故障排查

### Python 3 未找到
- macOS: `brew install python3`
- 或从 https://www.python.org/downloads/ 下载

### 权限错误
```bash
chmod +x scripts/install-hooks.sh
```

### Hooks 未生效
重启 Claude Code 应用程序。

## 配置选项

默认安装后：
- **模式：** audit（记录但不阻止）
- **日志：** `data/audit/hook-audit.jsonl`
- **文档：** `scripts/README.md`

修改模式：
```bash
# 临时（当前终端）
export SELF_EVO_ROLLOUT_MODE=pretool-enforce

# 永久（编辑配置）
# 编辑 scripts/hooks/config.json，改为 "pretool-enforce" 或 "full-enforce"
```
