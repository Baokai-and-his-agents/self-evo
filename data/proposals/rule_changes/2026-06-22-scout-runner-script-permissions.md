---
title: "规则变更提案：Scout Runner 脚本权限调整"
date: 2026-06-22
type: rule_change
status: pending_approval
requires_approval_from: jlcbk
related_issue: 7
---

# 规则变更提案：Scout Runner 脚本权限调整

## 背景

当前 `scripts/**` 目录在 `rules/RESOURCE_APPROVALS.yaml` 和 `rules/EXPLORATION_POLICY.md` 中全部受到保护，Agent 不可写入。这一保护设计是为了防止自动化修改关键基础设施代码，如 hooks、policy validators、schema validators 等安全敏感脚本。

然而，为了支持自主 Scout 垂直切片（Issue #7，项目候选 A.1-A.4），我们需要引入 Scout runner wrapper 脚本 `scripts/workers/scout_runner.py`，由 Agent 编写和维护。该脚本不涉及治理逻辑或 repo 安全策略，而是作为 Scout worker 的生命周期管理器：启动 Claude CLI 子进程、强制执行超时和调用数限制、捕获遥测、处理恢复。

当前全局保护使得 Agent 无法在 `scripts/` 下创建 Scout runner，阻碍了自主 Scout 的实现。

---

## 提议的规则变更

### 1. 缩小 `scripts/` 保护范围

将 `scripts/**` 的全局保护缩小为以下特定子目录和文件的保护：

**保持受保护（Agent 不可写）**：
- `scripts/hooks/**` — Git hooks 和生命周期回调
- `scripts/policy/**` — 治理策略验证器
- `scripts/validators/**` — Schema 和结构验证器
- `scripts/tests/test_*.py` — 测试套件主文件
- `scripts/validate_*.py` — 顶层验证入口点

### 2. 新增 Agent 可写区域

允许 Agent 在以下区域写入和修改：

**Agent 可写**：
- `scripts/workers/**` — Scout、Builder 等自主 worker 脚本
- `scripts/utils/**` — 通用工具函数（非治理逻辑）

### 3. Scout Runner 路径

Scout runner 脚本将创建在：
```
scripts/workers/scout_runner.py
```

该路径在项目候选文档 `data/proposals/project_candidates/2026-06-21-autonomous-agent-followups.md` 中明确指定为 Issue #A.1 的交付物。

---

## 安全边界

### Runner 不得绕过治理规则

Scout runner 必须：
- 只读检查 `rules/RESOURCE_APPROVALS.yaml` 和 `rules/EXPLORATION_POLICY.md`
- 仅将已批准的资源来源传递给 Scout worker
- 强制执行 `rules/` 中定义的限制（超时、调用数、扫描/保留上限）

### Agent 不得修改治理规则

Agent 和 worker 在任何情况下不得直接修改：
- `rules/RESOURCE_APPROVALS.yaml`
- `rules/EXPLORATION_POLICY.md`
- `rules/schemas/**`

若 Scout 需要访问新的资源来源（如 GitHub API、Hacker News、arXiv、Product Hunt），Agent 应：
1. 编写 `data/proposals/rule_changes/<date>-<topic>-resource-approval.md` proposal
2. 在相关 GitHub Issue 中请求人工审批
3. 由 `jlcbk` 修改或批准 `rules/` 中的规则文件后，Runner 才认为该来源正式批准

### 测试和验证脚本保护

测试套件主文件和顶层验证入口点保持受保护，以防止自动化绕过 CI/CD 检查：
- `scripts/tests/test_*.py` — 受保护
- `scripts/validate_*.py` — 受保护

Agent 可编写辅助测试工具在 `scripts/workers/` 或 `scripts/utils/` 下，但不得修改主测试套件。

---

## 实施计划

### 阶段 1：本 Proposal 获批准

本 proposal 需要 `jlcbk` 的明确批准后才能实施。

### 阶段 2：更新规则文件（人工执行）

在获得批准后，由 `jlcbk` 或授权人员更新：
- `rules/RESOURCE_APPROVALS.yaml` — 修改 `scripts/` 保护范围
- `rules/EXPLORATION_POLICY.md` — 记录新的 Agent 可写区域和边界

### 阶段 3：Agent 交付 Scout Runner

在规则更新后，Agent 可在 `scripts/workers/` 下创建 Scout runner，完成项目候选 Issue #A.1。

---

## 本 PR 不改规则

**重要**：本 PR (#8) 仅交付：
- 本 proposal 文档
- `.gitignore` 文件调整
- 测试文件
- 项目候选文档的同步更新

**本 PR 不修改** `rules/RESOURCE_APPROVALS.yaml` 或 `rules/EXPLORATION_POLICY.md`。这些规则文件的修改必须在本 proposal 获得 `jlcbk` 批准后，由人工在后续 PR 中完成。

---

## 验收标准

- [ ] 本 proposal 由 `jlcbk` 审查并批准或修订
- [ ] 批准后，`rules/RESOURCE_APPROVALS.yaml` 更新保护范围
- [ ] 批准后，`rules/EXPLORATION_POLICY.md` 记录新边界
- [ ] Agent 能在 `scripts/workers/` 下创建 Scout runner
- [ ] 测试验证：Agent 仍不能修改 `scripts/hooks/`、`scripts/policy/`、`scripts/validators/`
- [ ] 项目候选 Issue #A.1 解除阻塞

---

## 风险评估

**风险**：低

- Scout runner 不涉及治理逻辑，仅作生命周期管理
- 安全敏感脚本（hooks、policy、validators）保持受保护
- Agent 仍需人工批准才能访问新资源来源
- 测试套件主文件保持受保护

**缓解**：
- 明确 Runner 只读 `rules/`，不得修改
- Agent 通过 proposal 流程请求新来源批准
- 人工审查所有 `scripts/workers/` 提交

---

## 相关文档

- 项目候选：`data/proposals/project_candidates/2026-06-21-autonomous-agent-followups.md`
- Issue #7 研究报告：`data/exploration/daily_reports/2026-06-21-autonomous-agent-ecosystem.md`
- 当前治理规则：`rules/RESOURCE_APPROVALS.yaml`、`rules/EXPLORATION_POLICY.md`

---

**提案人**：Agent (Scout worker 01)  
**审批人**：jlcbk  
**状态**：待审批  
**前置条件**：Issue #A.1 实施需本 proposal 批准
