# 自学习和执行的自主 Agent 项目蓝图

日期：2026-06-18
状态：草案 v0.5

这个文件用于沉淀我们当前对“自学习和执行的自主 agent”的共识。后续所有设计调整、实现拆分、权限规则和记忆系统选择，都可以在这个文件基础上继续演化。

## 0. v0.5 已确认设计决策

v0.5 在 v0.4 的基础上，补充施工后的仓库结构和 agent 操作说明书分层：

- 第一版先做单 worker，由用户在本地手动启动 Code worker，根据本项目指导文件工作；暂不要求后台自动调度。
- `rules/START_HERE.md` 是 agent 的唯一启动入口。用户打开 Claude Code 后，只需要让它读取这个文档，它就能知道还要加载哪些规则、去哪里找任务、如何 claim、如何执行和如何收尾。
- `START_HERE.md` 是入口路由和强约束摘要，不替代完整规则文件；细节仍由 `AGENT_PROTOCOL.md`、`PERMISSIONS.yaml`、`TASK_POLICY.md`、`GITHUB_POLICY.md` 等文件承载。
- `rules/AGENT_PROTOCOL.md` 是完整操作说明书，负责说明 agent 如何与这个仓库协作。
- 仓库施工时应先搭好 rules / data / state / .github 的基础骨架，再逐步补充规则内容和运行数据。
- 任务入口以 GitHub Issue 为主；本地任务文件作为镜像、摘要和离线备份。
- 多 worker 不在第一版实际启用，但 Issue label、claim、lease、worker identity 和分支命名需要提前预留。
- 学习执行任务暂不固定笔记格式，但必须保留来源、整理笔记、实验或 demo 证据、可复用结论和下一步建议。
- 规则区和数据区必须分离：`rules/` 是只读规则区，agent 只能读取和提出修改建议，不能直接修改；`data/` 是 agent 按规则自由写入的工作区。
- 所有未明确授权的外部资源调用都需要用户确认；批准过的资源写入 `rules/RESOURCE_APPROVALS.yaml`，后续 worker 可按 scope 自动复用。
- 审批动作以用户修改 `rules/` 中的规则文件为准，agent 看到状态为 approved 后才认为正式批准。
- 记忆默认进入热区；从热区降入冷区前必须通知用户，并允许用户要求调回热区。
- 主动探索可以适当发散，但每次探索必须留下轨迹，供用户后续 review 和偏好标注。
- 探索必须优先复用已有成果，不重复造轮子。agent 在自研方案前，应先寻找成熟教程、工具、GitHub 项目、案例、模板和已有 workflow，并评估是否可直接采用或组合。
- GitHub 身份采用 agent 独立账号执行、人类账号审批的模式；agent 账号可以有写权限，但不应拥有 admin 或 bypass branch protection 权限。
- `rules/**` 通过 CODEOWNERS、branch protection / rulesets 保护：agent 可以提交规则修改 PR，但必须由人类账号审批后才能合并。

## 1. 项目定位

这个项目不是一个普通的收藏夹、RAG 知识库或聊天机器人，而是一个长期运行的个人执行系统：

> 一个能主动学习、主动侦察、主动拆解任务、主动执行低风险实验，并通过文档和用户保持长期协作的自主 agent。

核心目标是把用户的松散意图、链接、技能名称、项目想法，持续转化为：

- 可执行任务
- 可复用技能
- 本地实验结果
- 项目机会判断
- 长期记忆和决策记录

一句话：

> 它不是等用户整理资料，而是在空闲时间主动把值得学习的知识和值得验证的机会变成行动资产。

## 2. 核心运行模式

系统采用“GitHub Issue 通信 + 本地 Code worker 执行 + 规则文件约束”的模式。

```text
用户
  ↓
GitHub Issue / 本地规则文件
  ↓
用户本地启动 Code worker
  ↓
一个或多个 Worker
  ↓
学习、执行、实验、汇报、记忆更新
```

第一版用户主要通过 GitHub Issue 投递和追踪任务，同时通过本地文件沉淀长期记忆：

- 把任务、链接、技能名写入 GitHub Issue。
- 用户在本地启动 Code worker；worker 读取本项目的规则文件和 open issue，claim 一个任务并执行。
- agent 把过程记录、阻塞点、需要确认的动作写回 issue comment 和 data/tasks/REVIEW.md。
- 用户可以通过 issue comment、label 或本地控制文件继续指导它。
- 本地 rules / data 负责规则约束、运行摘要、技能沉淀和决策记录。

这让系统不依赖某一次聊天上下文，可以跨轮次、跨 worker、跨日期持续运行。GitHub Issue 承担当前任务状态和审计，本地文件承担长期记忆和可人工修改的事实源。

## 3. 第一性原则

### 3.1 文件是事实源

长期记忆、任务队列镜像、决策记录、技能沉淀都应优先存在于 Git 管理的 Markdown / YAML / JSONL 文件中。当前任务状态的第一事实源是 GitHub Issue，本地文件负责镜像、复盘和长期沉淀。

外部记忆系统、向量库、OpenViking、GBrain、SQLite FTS 都只能作为增强层，而不能成为唯一事实源。

原因：

- 用户可以直接阅读和修改。
- Git 可以追踪历史。
- 多个 agent 可以基于同一套文件接力。
- 外部系统失效时，核心记忆不会丢。

### 3.2 规则区和数据区分离

系统必须区分规则区和数据区：

```text
rules/
  规则区。定义 agent 能做什么、不能做什么、如何审批、如何写入数据。
  agent 只能读取和遵守，不能直接修改。

data/
  数据区。存放任务过程、学习材料、探索记录、实验结果、候选记忆。
  agent 可以在遵守 rules 的前提下自由写入。
```

规则区是系统的约束层，一旦确定就不能由 agent 自行变动。任何规则变更只能由 agent 写入 `data/proposals/rule_changes/`，等待用户审阅。只有用户亲自修改 `rules/**`，才视为规则正式变更。

数据区是 agent 的工作区，可以先保持较高自由度。第一版不强制每类数据使用统一模板，但要求所有重要输出都能追溯到 GitHub Issue、来源、时间和 worker identity。

### 3.3 单入口启动文档

Claude Code 每次打开时上下文可能为空，因此必须有一个单入口启动文档：

```text
rules/START_HERE.md
```

用户启动 agent 时，只需要给出固定指令：

```text
Read rules/START_HERE.md and follow it exactly.
```

`START_HERE.md` 的职责是：

- 声明当前身份：本地 Code worker，不是自由聊天助手。
- 列出启动后必须读取的规则文件。
- 摘要最重要的硬约束，尤其是不得直接修改 `rules/**`。
- 告诉 agent 如何寻找 GitHub Issue、claim 一个任务、创建工作分支。
- 告诉 agent 如何处理未批准资源、规则变更和不确定情况。
- 告诉 agent 在探索和构建前先查找已有成熟成果，避免重复造轮子。
- 告诉 agent 结束前必须写入哪些记录。

`START_HERE.md` 不应该变成完整手册。它应该保持短小，作为入口路由和启动清单；细节继续由各规则文件承载。

### 3.4 每次运行都必须可复盘

agent 每次 tick 都必须留下：

- 做了什么
- 为什么做
- 读了哪些资料
- 改了哪些文件
- 遇到哪些错误
- 哪些事情需要用户确认
- 哪些记忆建议写入长期记忆

不能只留下漂亮总结，必须保留足够证据。

### 3.5 主动性必须受控

agent 可以主动学习和探索，但不能无限浏览、无限总结、无限开新坑。

必须有：

- 任务预算
- 时间预算
- 成本预算
- 权限边界
- 每轮最多推进的任务数
- Review Queue

### 3.6 先低风险执行，再高风险确认

默认允许 agent 自动做以下低风险动作，但前提是没有触发未授权外部资源调用：

- 读取已批准范围内的公开资料
- 总结已批准范围内的链接
- 写本地笔记
- 创建本地 demo
- 在 sandbox 跑实验
- 生成计划和候选方案
- 在 GitHub 规则允许范围内 push agent 分支
- 创建 draft PR 作为可审计交付物

默认需要用户确认：

- 所有未明确授权的外部资源调用
- 安装全局软件
- 改系统环境变量
- 使用私人账号
- 使用 API token 或私有凭证
- 使用服务器、云资源、GPU、付费模型或其它计算资源
- push 到 main、受保护分支或非 agent 命名分支
- 将 draft PR 标记为 ready for review
- 合并 PR
- 部署到生产环境
- 花钱
- 联系真实用户或客户

默认禁止：

- 删除重要资料
- 读取或上传私钥、token、密码
- 执行链上交易
- 批量发帖或自动私信
- 绕过平台限制
- 在未确认情况下公开发布内容

### 3.7 资源审批表

所有外部资源授权都应记录在一个可审计的资源审批表中，建议路径：

```text
rules/RESOURCE_APPROVALS.yaml
```

worker 在使用任何外部资源前必须先查表：

1. 如果资源不存在、状态不是 approved、超出 scope、超出预算或已过期，写入 REVIEW 并等待用户确认。
2. 如果资源已批准，且本次用途在 scope 和 budget 内，可以自动使用。
3. token、密码、私钥等敏感值不能写入审批表，只能记录环境变量名、凭证来源说明或人工配置说明。
4. 每次使用外部资源后，需要在 run log 中记录资源 id、用途、估算成本和结果。

审批动作以用户修改 `rules/RESOURCE_APPROVALS.yaml` 为准。agent 不能自己把资源状态改成 approved，也不能修改任何 `rules/**` 文件来为自己授权。

示例：

```yaml
resources:
  - id: openai-api
    type: api
    provider: OpenAI
    status: approved
    scope:
      - read_docs
      - run_low_cost_eval
    credential_ref: env:OPENAI_API_KEY
    cost_limit_usd_per_day: 5
    runtime_limit_minutes_per_day: null
    expires_at: null
    approved_by: user
    approved_at: 2026-06-18
    notes: 只记录凭证引用，不记录 token 本身。
```

这个表会随着用户审批逐渐增长。第一阶段需要用户确认的事情会多一些；当常用资源都被明确授权后，worker 可以在边界内更自动地执行。

常见资源条目可以包括 `public-web-read`、`github-api-read`、`openai-api`、`cloud-vm`、`gpu-runtime` 等。公共网络读取也应作为资源被明确批准，而不是被隐含允许。

## 4. 文档通信协议

第一版任务主入口是 GitHub Issue。本地文件分为规则区和数据区：规则区定义边界，数据区承载执行过程和记忆沉淀。

建议建立如下目录：

```text
rules/
  START_HERE.md            agent 空上下文启动入口
  AGENT_PROTOCOL.md        agent 行为协议
  PERMISSIONS.yaml         权限边界和禁区
  RESOURCE_APPROVALS.yaml  已批准外部资源
  TASK_POLICY.md           任务认领、执行和验收规则
  MEMORY_POLICY.md         热区、冷区和长期记忆规则
  EXPLORATION_POLICY.md    主动探索和复审规则
  GITHUB_POLICY.md         GitHub 身份、PR、CODEOWNERS 规则

data/
  tasks/
    INBOX.md               本地临时输入和离线备份，不是第一任务入口
    TASKS.md               GitHub Issue 的本地镜像和摘要
    REVIEW.md              等待用户确认的事项
    DONE.md                已完成任务摘要

  runs/                    agent 每轮执行摘要和证据
  notes/                   学习笔记和自由整理材料
  skills/                  可复用技能沉淀
  memory/                  hot / cold 长期记忆
  proposals/               资源、规则变更和跨模块提案
  exploration/             主动探索轨迹、复审标签和 reuse maps

state/
  heartbeat.json           worker 心跳
  locks/                   文件锁和任务锁
  claims/                  worker 对任务的认领记录

.github/
  CODEOWNERS               rules/** 的人类审批边界
  ISSUE_TEMPLATE/          GitHub Issue 任务入口模板
  pull_request_template.md agent PR 交付说明模板

scripts/
  README.md                后续放置本地辅助脚本，MVP 可先为空

docs/
  autonomous-agent-blueprint.md
  ARCHITECTURE.md          当前系统架构
  DECISIONS.md             已确认的长期设计决策摘要
```

### 4.1 rules/START_HERE.md

`START_HERE.md` 是用户每次打开 Claude Code 时给 agent 的唯一入口。推荐首句固定为：

```text
Read rules/START_HERE.md and follow it exactly.
```

这个文件应该集中说明 agent 的工作方式，但只保留启动所需的关键信息。建议结构：

```md
# START HERE

## Identity
You are the local Code worker for this repository.

## Load First
Read these before doing anything:
1. rules/AGENT_PROTOCOL.md
2. rules/PERMISSIONS.yaml
3. rules/RESOURCE_APPROVALS.yaml
4. rules/TASK_POLICY.md
5. rules/GITHUB_POLICY.md

## Hard Rules
- Do not modify rules/** directly.
- Work on exactly one claimed GitHub Issue per run.
- If a rule change is needed, write data/proposals/rule_changes/*.md.
- If a resource is not approved, request approval instead of using it.
- Before building from scratch, search for existing mature solutions first.

## Task Flow
1. Find open GitHub Issues.
2. Claim one suitable issue.
3. Write a claim comment with worker identity, branch, lease_until, and run id.
4. If the issue requires exploration, first survey existing tutorials, tools, examples, GitHub repositories, templates, and workflows.
5. Work only within approved permissions.
6. Record evidence under data/**.

## Before Stopping
Write:
1. GitHub Issue progress or completion comment.
2. data/runs/<date>/<run-id>.summary.md.
3. data/tasks/REVIEW.md if anything needs human confirmation.
```

`START_HERE.md` 可以引用其它规则文件，但不应复制全部细节。这样 agent 的启动上下文集中，规则细节又能保持模块化。

### 4.2 rules/AGENT_PROTOCOL.md

`AGENT_PROTOCOL.md` 是项目给 agent 的完整操作说明书。它不负责做启动入口，而是解释 agent 如何长期与这个仓库协作。

`START_HERE.md` 和 `AGENT_PROTOCOL.md` 的区别：

```text
START_HERE.md
  入口卡片。解决 Claude Code 空上下文启动问题。
  目标是让 agent 知道先读什么、怎么开始、哪些硬规则不能碰。

AGENT_PROTOCOL.md
  完整说明书。解释项目目标、工作方式、任务流、权限边界、记录要求和失败处理。
  目标是让 agent 理解如何与这个项目持续协作。
```

`AGENT_PROTOCOL.md` 第一版应至少包含：

```md
# Agent Protocol

## Project Purpose

## Worker Identity

## How To Work With This Repository

1. Load startup rules.
2. Inspect GitHub Issues.
3. Claim exactly one issue.
4. Check permission and resource approvals.
5. Work under data/** by default.
6. Never modify rules/** directly.
7. Produce evidence and run summary.
8. Ask for human approval when blocked.
9. Close or update the issue.

## Rule And Data Boundary

## GitHub Issue Workflow

## Exploration Workflow

## Reuse Existing Work First

## Resource Approval Workflow

## Run Logs And Evidence

## Failure And Uncertainty Handling
```

这样 agent 不需要知道之前的讨论历史。只要读 `START_HERE.md`，再按要求读 `AGENT_PROTOCOL.md`，就能知道怎样与项目协作。

### 4.3 data/tasks/INBOX.md

用户可以随手写本地输入，不需要太结构化。第一版中，长期任务仍应优先创建为 GitHub Issue；INBOX 更适合临时草稿、离线输入或还没准备进入任务队列的想法。示例：

```md
## 2026-06-16

- 学习 Playwright browser automation
- 看这个项目是否值得做：https://example.com/project
- 研究 OpenViking 是否适合作为长期记忆后端
```

### 4.4 data/tasks/TASKS.md

TASKS.md 不是第一事实源，而是 GitHub Issue 的本地镜像、摘要和离线备份。worker 可以从 Issue 同步出结构化任务摘要。示例：

```md
## T-20260616-001

type: skill
status: open
priority: high
goal: 学习 Playwright browser automation，并沉淀成可复用技能卡
source:
  - https://example.com/playwright-doc
acceptance:
  - 产出一份 skill note
  - 跑通一个最小 demo
  - 写出 3 个可自动化场景
permission: read_write_sandbox
owner: unclaimed
github_issue: 12
worker_identity: null
lease_until: null
created_at: 2026-06-16
```

### 4.5 data/tasks/REVIEW.md

agent 不能直接做的动作写入这里。示例：

```md
## R-20260616-001

task: T-20260616-001
request: 是否允许安装 Playwright 浏览器依赖？
risk: 会安装本地运行依赖，但不涉及系统账户或远程发布。
recommended_action: approve
```

### 4.6 学习执行任务最低证据标准

学习任务的输出形式不需要第一版定死，允许 worker 根据主题自行组织。但每个学习执行任务至少要留下：

- 原文链接、文档、仓库、论文或其它来源记录。
- 整理后的学习笔记，不能只保留原文摘录。
- worker 自己判断的重点、适用场景、限制和常见坑。
- 如果主题可执行，至少一个最小 demo、命令记录、实验结果或失败复现。
- 可进入长期记忆的候选条目。
- 下一步建议，包括继续深挖、转为构建任务、暂缓或归档。

这些内容可以写在 Issue comment、本地 run summary、data/memory/proposals 或 skill note 中。验收先看证据是否足够支撑用户复审，后续再逐步沉淀更固定的格式。

### 4.7 规则变更提案

agent 如果认为某条规则、权限、资源审批、记忆策略或探索策略需要调整，不能直接修改 `rules/**`。它只能写入：

```text
data/proposals/rule_changes/<date>-<short-title>.md
```

提案至少包含：

- 想修改的规则文件和规则项。
- 修改原因。
- 建议的新规则文本。
- 风险和回滚方式。
- 相关 Issue、运行记录或证据。

用户审阅后，如果同意，由用户亲自修改 `rules/**`。agent 在后续运行中读取新 rules 文件后，才可以按新规则执行。

## 5. GitHub 协调控制平面

v0.5 确认：第一版任务入口以 GitHub Issue 为主。GitHub 是人和 agent、多 agent 之间的共享状态协调层；本地 rules / data 是规则、长期记忆和执行证据层。

需要明确 GitHub 的定位：

```text
GitHub 负责：
  - 任务登记
  - 状态流转
  - 所有权认领
  - 分支和 PR 审计
  - 人类确认
  - 多 agent 防冲突

本地 worker 负责：
  - 实际阅读
  - 实际学习
  - 实际实验
  - 实际代码修改
  - 实际总结和记忆沉淀
```

不要把 GitHub 当成唯一记忆系统，也不要把 GitHub Actions 当成长跑 agent 主体。GitHub 更适合作为控制平面和审计面。

第一版推荐使用 GitHub Issue，而暂不强依赖 GitHub Project。Issue label、comment 和 assignee 足够支撑任务流转；Project 可以在任务量增大后再加入。

Issue 模板建议包含：

```md
## Goal

## Sources

## Acceptance Evidence

## Permission Level

## Resource Requests

## Notes
```

worker 必须把 claim、阶段性进展、阻塞点、资源审批请求和完成摘要写回 Issue comment。涉及长期记忆的内容，再同步进入 data/memory/proposals。

### 5.1 GitHub 身份与审批模型

第一版推荐使用两个身份：

```text
agent GitHub account
  负责 claim issue、写 comment、push agent 分支、创建 PR。
  可以拥有 repository write 权限。
  不应拥有 admin 权限，也不应拥有 bypass branch protection 权限。

human GitHub account
  负责审批规则变更、资源授权、PR 合并和高风险动作。
  是 rules/** 的 code owner。
```

这样可以清楚区分哪些操作是 agent 执行，哪些操作是人类审批。agent 使用独立账号提交的 Issue comment、commit 和 PR，天然成为审计记录。

如果早期临时使用用户个人 token，也必须在每次 claim 和 run summary 中写明 worker identity，避免后续无法区分人类操作和 agent 操作。

### 5.2 rules/** 的 GitHub 保护

GitHub 不提供传统文件系统意义上的“给某个账号仓库写权限，但某个目录只读”的 ACL。推荐用 PR 流程实现只读边界：

1. agent 账号可以创建分支和 PR。
2. `main` 禁止直接 push，必须通过 PR 合并。
3. `.github/CODEOWNERS` 指定 `rules/**` 归人类账号所有。
4. 分支保护或 ruleset 要求 code owner review。
5. agent 账号不能拥有 admin 或 bypass branch protection 权限。

示例 CODEOWNERS：

```text
/rules/ @human-github-username
/.github/CODEOWNERS @human-github-username
```

这样 agent 可以提交规则修改 PR，但不能自己合并。只有人类账号批准后，规则变更才能进入 `main`。

更强的可选方案是 GitHub push rulesets：按路径限制包含 `rules/**` 的 push。这个方案更硬，但可能连 agent 的规则修改提案分支也阻止推送，因此第一版优先使用 CODEOWNERS + branch protection。

### 5.3 GitHub 对象映射

推荐映射：

```text
Issue
  一个可认领任务。

Label
  任务类型、权限等级、状态、worker 类型。

Assignee
  人类 owner，或 agent 独立 GitHub 账号。

Project
  看板视图，用于展示 backlog / claimed / in-progress / review / done。

Branch
  某个 agent 对某个任务的独立工作区。

Pull Request
  agent 的可审计输出和合并请求。

Issue comment
  agent 的进展日志、阻塞点、确认请求。
```

### 5.4 任务标签建议

```text
type:scout
type:learn
type:build
type:review
type:memory

status:open
status:claimed
status:running
status:blocked
status:review
status:done

agent:scout
agent:learner
agent:builder
agent:reviewer

permission:read-only
permission:sandbox
permission:repo-write
permission:external-resource
permission:needs-human

risk:low
risk:medium
risk:high
```

### 5.5 防止两个 agent 做同一个任务

每个 worker 在开始工作前必须执行 claim 流程：

```text
1. 查询 open issue。
2. 按 label 和优先级选择候选任务。
3. 检查 issue 是否已有 status:claimed 或 status:running。
4. 尝试写入 claim comment。
5. 尝试更新 label 为 status:claimed。
6. 创建 state/claims/<issue-number>.json。
7. 创建独立分支 agent/<worker>/<issue-number>-<slug>。
8. 只有 claim 成功后才能开始执行。
```

claim comment 示例：

```md
Agent claim:
- worker: learner-worker-01
- lease_until: 2026-06-16T18:30:00+08:00
- branch: agent/learner/12-playwright-skill
- local_run: 2026-06-16/tick-004
```

如果 worker 崩溃，lease 超时后其他 worker 可以接手，但必须先读旧 comment、分支和 run log。

### 5.6 模块归属

多个 agent 可以长期负责不同模块，减少冲突：

```text
scout-worker
  labels: type:scout
  paths: data/exploration/**, data/sources/**, data/memory/summaries/daily/**

learner-worker
  labels: type:learn
  paths: data/skills/**, data/notes/**, data/memory/hot/skills/**

builder-worker
  labels: type:build
  paths: app/**, scripts/**, tests/**

reviewer-worker
  labels: type:review
  paths: data/tasks/REVIEW.md, data/proposals/**, PR reviews
```

每个 worker 应该有默认可写路径。跨路径修改需要升级到 review 或人工确认。任何 worker 都不能直接修改 `rules/**`。

### 5.7 PR 作为交付物

凡是涉及代码、核心文档或长期记忆的修改，推荐通过 PR 完成：

```text
Issue -> agent branch -> commits -> draft PR -> reviewer agent -> human merge
```

PR 模板应该包含：

```text
Linked issue
Worker identity
Goal
Files changed
Evidence / sources
Tests or checks
Risks
Memory updates proposed
Needs human confirmation
```

默认创建 draft PR。只有 reviewer-worker 或用户确认后，才进入可合并状态。

### 5.8 GitHub 与本地文档的关系

GitHub 是跨 agent 协调层，本地文档是项目记忆和执行协议层。

两边需要同步，但职责不同：

```text
GitHub Issues / Projects
  当前任务状态、所有权、PR、审计。

rules / data
  rules 保存行为协议和权限边界。
  data 保存技能、经验、运行摘要、候选记忆和探索记录。
```

同步规则：

- GitHub Issue 创建后，由 worker 同步摘要到 data/tasks/TASKS.md。
- data/tasks/INBOX.md 中的新任务，可以由 worker 转成 GitHub Issue；转完后写回 issue 链接。
- worker 的 claim、进展、阻塞、资源审批请求和完成摘要必须写入 Issue comment。
- 每次 tick 的本地证据、运行摘要和工具记录进入 data/runs。
- 可复用技能、偏好、项目结论先进入 data/memory/proposals，review 后再合并到 data/memory/hot。
- 规则变更建议只能进入 data/proposals/rule_changes，不能直接修改 rules。
- 重要长期决策摘要进入 docs/DECISIONS.md 或 data/memory/hot/project/decisions.md。

### 5.9 适合使用 GitHub 的部分

适合：

- 任务队列
- 所有权认领
- 状态看板
- 代码修改审计
- 人类 review
- 多 agent 分工
- release / milestone 管理

不适合：

- 高频 heartbeat
- 大量原始日志
- 大量网页缓存
- 长期语义检索
- 私密 token 或敏感资料
- 每一步 tool call 细节

这些仍然应留在本地 state、data/runs 或专门的索引系统里。

## 6. 本地 Code Worker 设计

第一版先运行单个本地 Code worker，用手动启动的一次工作循环测试学习和执行闭环。worker 不需要自己启动后台服务，也不要求无人值守定时运行；用户在本地启动 Code，让它读取本项目规则文件并按 GitHub Issue 工作。

一次工作循环建议：

```text
用户本地启动 Code worker
读取 rules/START_HERE.md
按 START_HERE 加载必要规则文件
读取 GitHub open issues
每次只 claim 1 个任务
每次有 max turns / max cost / max runtime
结束前必须写 Issue comment、data/runs 和 data/tasks/REVIEW.md
```

虽然第一版只启用一个 worker，但任务协议必须预留多 worker：

- 每次运行都带 worker identity，例如 `learner-worker-01`。
- 每个任务都走 claim / lease 流程，即使当前没有竞争。
- 分支命名使用 `agent/<worker>/<issue-number>-<slug>`。
- label 中保留 `agent:*`、`type:*`、`status:*` 和 `permission:*`。
- 本地 state/claims 和 Issue comment 都记录同一份 claim 信息。
- worker 启动和结束时检查 `rules/**` 是否被自己修改；如果发现被修改，必须停止并写入违规说明，不能提交该修改。

后续可以扩展多个 worker：

```text
scout-worker
  负责主动侦察、阅读外部信息源、发现机会。

learner-worker
  负责学习技能、整理文档、跑最小 demo。

builder-worker
  负责实现代码、创建脚手架、修复问题。

reviewer-worker
  负责复核其他 worker 的结果、检查风险、整理长期记忆建议。
```

多 worker 必须使用 claim / lock 机制，避免同时编辑同一个任务或同一批文件。

## 7. Supervisor 与 Hooks

第一版不强制实现外层 supervisor。Code worker 由用户本地手动启动，主要依靠 `rules/**`、GitHub 保护和工作协议约束行为。

后续如果要提高自动化和违规拦截能力，可以增加一个很薄的 supervisor。

未来 Supervisor 职责：

- 可选地定时唤醒 worker
- 注入必要环境变量和 PATH
- 检查 Claude Code 是否能访问关键工具
- 控制每次运行预算
- 记录 worker 心跳
- 处理任务锁
- 检查输出是否符合协议
- 检查 `rules/**` 是否被 agent 直接修改

Hooks 职责：

```text
SessionStart
  加载 rules/START_HERE.md 和必要规则文件、检查环境、写 heartbeat。

PreToolUse
  拦截危险命令、越界路径、rules/** 写入、敏感文件读取、部署、付款、删除等动作。

PostToolUse
  记录命令、文件变化、失败信息。

Stop
  强制检查是否写入 Issue comment、data/runs、data/tasks/REVIEW.md、任务状态。

FileChanged
  对关键文档做格式检查和冲突检查。
```

特别注意：工具可用性不能只由外层 shell 判断。需要让 Claude Code worker 自己执行检查。Windows 上可能出现主 shell 能找到工具，但 Claude Code 子进程继承不到 PATH 的情况。

## 8. 记忆系统

记忆系统采用“文件为主、热冷分层、索引为辅、定期压缩、可人工纠偏”的设计。

```text
data/memory/
  hot/
    profile/
      user_preferences.md
      interest_map.yaml
      negative_patterns.md

    project/
      goals.md
      architecture.md
      decisions.md
      open_questions.md

    skills/
      playwright/
        SKILL.md
        examples.md
        commands.md
        mistakes.md

    learnings/
      facts.md
      mistakes.md
      recipes.md
      experiments.md

  cold/
    archive/
    old_skills/
    old_runs/
    old_sources/

  sources/
    github/
    hackernews/
    arxiv/
    producthunt/
    web_clips/

  summaries/
    daily/
    weekly/
    monthly/

  proposals/
    memory/
    cooldown/

  index/
    self_evo.sqlite
    embeddings/

data/runs/
  2026-06-18/
    tick-001.jsonl
    tick-001.summary.md

data/exploration/
  raw/
  daily_reports/
  review_labels/
  preference_analysis/
```

### 8.1 热区和冷区

默认所有新长期记忆先进入热区。热区内容是 worker 启动和执行任务时可以优先读取的高频上下文。

冷区用于保存低频、过期、暂时不用但仍有保留价值的材料。冷区内容不能默认加载，需要通过检索、人工指定或探索任务进一步挖掘。

从热区转入冷区前，worker 必须：

1. 写入 data/memory/proposals/cooldown/*.md，说明候选条目、原因、最后使用时间和影响。
2. 在 data/tasks/REVIEW.md 或对应 GitHub Issue 中通知用户。
3. 等用户确认后再移动到 data/memory/cold。

如果用户认为冷却不恰当，worker 应按用户意见把内容留在热区，或从 data/memory/cold 调回 data/memory/hot，并记录原因。

### 8.2 长期记忆写入规则

worker 不应直接随意改长期记忆。推荐流程：

```text
worker 观察和执行
  ↓
写 data/memory/proposals/*.md
  ↓
reviewer 或 supervisor 复核
  ↓
合并到 data/memory/hot/profile、data/memory/hot/project、data/memory/hot/skills 或 data/memory/hot/learnings
```

这样可以防止一次偶然失败被写成永久规则。

### 8.3 启动时加载上下文

每次 worker 启动时不应该加载全部记忆，而是按优先级加载：

```text
1. rules/START_HERE.md
2. rules/AGENT_PROTOCOL.md
3. rules/PERMISSIONS.yaml 和 rules/RESOURCE_APPROVALS.yaml
4. data/memory/hot/profile/user_preferences.md
5. data/memory/hot/project/goals.md 和 data/memory/hot/project/decisions.md
6. 当前任务
7. 相关 data/memory/hot skill memory
8. 最近 1-3 次 run summary
9. 必要时检索 data/memory/cold 或 index
```

### 8.4 LLM Wiki / OpenViking / GBrain 的位置

当前判断：

```text
LLM Wiki
  立刻采用它的思想：Markdown wiki、持续整合、交叉链接、矛盾标记。

OpenViking
  第二阶段作为 context backend / MCP memory 适配器试验。
  不作为第一版唯一事实源。

GBrain
  后期作为知识图谱、synthesis、gap analysis 增强层试点。
  不在 MVP 阶段绑定核心架构。
```

核心原则：

> Markdown / YAML 文件是 canonical memory。外部记忆系统只能做增强层。

## 9. 主动侦察模块

项目后续应加入 Autonomous Scout，让 agent 在空闲时间主动寻找值得学习和验证的内容。

v0.5 对探索的态度是：允许适当发散，但必须可复审。Token 和网络资源充裕时，可以扩大阅读和扫描范围；真正的约束不是“少看”，而是“看过什么、为什么看、为什么保留或丢弃”必须记录下来。

探索的核心原则是：不要重复造轮子。很多任务已经有成熟教程、开源工具、案例拆解、模板、攻略和完整 workflow。agent 在尝试自研或重新设计前，必须先做 existing work survey：

```text
1. 找成熟教程和最佳实践。
2. 找可复用工具、库、模板、GitHub 项目。
3. 找高质量案例和复盘。
4. 找已有素材来源和版权规则。
5. 评估直接采用、组合改造、自研补齐三种路径。
```

只有当已有成果无法满足目标，或组合成本高于自研时，agent 才应提出自研方案。即使需要自研，也要说明“已有成果为什么不够用”。

模块：

```text
Autonomous Scout
  ├─ Topic Watcher
  ├─ Source Crawler
  ├─ Trend Detector
  ├─ Opportunity Finder
  ├─ Skill Gap Finder
  ├─ Experiment Generator
  └─ Report Generator
```

第一批低风险数据源：

- GitHub Search / REST API
- Hacker News API
- arXiv API
- Product Hunt API
- 官方文档 changelog / RSS

第二阶段再考虑：

- X / Twitter
- Reddit
- linux.do
- Discord / Telegram

主动侦察的输出不应该是信息流，而应该是决策流：

```text
一份已有成果地图 reuse map
1 个最值得做的实验
1 个最值得学的技能
1 个最值得观察的商机
若干证据链接
```

reuse map 至少包含：

- 可直接复用的教程、工具、模板或项目。
- 可组合改造的方案。
- 不建议使用的方案及原因。
- 仍然缺失、需要 agent 自行补齐的部分。
- 推荐下一步：直接采用、先试用、继续调研、还是自研。

每次探索还应留下探索轨迹：

```text
data/exploration/raw/
  原始链接、查询词、API 返回摘要、保留和丢弃理由。

data/exploration/daily_reports/
  每日探索摘要，突出值得继续看的内容。

data/exploration/review_labels/
  用户 review 后的标注，例如 relevant、irrelevant、deep-dive、pause。

data/exploration/preference_analysis/
  worker 对用户偏好的阶段性总结：为什么某些内容相关，为什么另一些偏题。
```

后续可以增加 preference learner：定期读取用户 review labels，总结主题边界、兴趣漂移和不相关模式，用来减少越学越散的问题。

### 9.1 主题探索程序

当 GitHub Issue 描述的是一个长期方向，而不是一个明确的一次性任务时，agent 应将其识别为 exploration program。

非规范示例：

```text
做财经故事视频：用讲故事的方式介绍金融领域的著名历史事件或商战。
```

这个例子只用于说明 agent 如何处理“长期方向型 Issue”。它不是项目默认主题，不是固定任务方向，也不能被写入规则文件作为 agent 的领域偏好。实际运行时，agent 必须以当前 GitHub Issue 的内容为准。

这类 Issue 的默认流程：

```text
1. 写 exploration brief
   - 用户想做什么
   - 目标产物是什么
   - 当前能力缺口是什么
   - 需要探索哪些方向
   - 哪些资源或账号可能需要审批

2. 拆 capability map
   - 领域知识
   - 方法论和最佳实践
   - 工具链
   - 数据、素材或输入来源
   - 权限、版权、成本和风险
   - 生产或执行 pipeline

3. 做 existing work survey
   - 优先找成熟教程、工具、模板、GitHub 项目、案例复盘和现成 workflow
   - 输出 reuse map
   - 判断哪些可以直接采用，哪些需要组合，哪些必须自研

4. 转成候选子任务
   - type:scout 搜集候选方向、案例和已有成果
   - type:learn 学习关键方法和工具链
   - type:learn 调研输入来源、权限和风险限制
   - type:build 制作最小样片或 demo
   - type:review 请求用户选择方向或方案

5. 输出决策方案
   - 3-5 个可选方案
   - 每个方案的优点、风险、难度、资源需求和第一步
   - 明确推荐项
```

agent 不应在看到长期方向后直接尝试完成最终产品。它应先把方向转为可复审的学习和执行路线，再由用户选择进入哪个制作方案。

## 10. 探索预算

主动 agent 必须有预算机制。v0.5 中预算不是为了压制探索，而是为了控制安全边界、资源上限和复盘粒度。由于用户允许较充裕的 token 和网络资源，探索预算可以相对宽松，但外部付费资源仍必须遵守资源审批表。

示例：

```yaml
daily:
  max_sources: 20
  max_items_scanned: 2000
  max_items_kept: 80
  max_experiments: 4
  max_runtime_minutes: 180
  max_cost_usd: use_resource_approval_table

weekly:
  max_new_skills: 3
  max_project_candidates: 10
  max_project_sprints: 2
```

同时需要好奇心比例：

```yaml
curiosity:
  exploit_ratio: 0.70
  explore_ratio: 0.20
  random_ratio: 0.10
```

## 11. 施工后的项目结构

按当前蓝图施工后，仓库第一版应接近以下结构：

```text
self-evo/
  docs/
    autonomous-agent-blueprint.md
    ARCHITECTURE.md
    DECISIONS.md

  rules/
    START_HERE.md
    AGENT_PROTOCOL.md
    PERMISSIONS.yaml
    RESOURCE_APPROVALS.yaml
    TASK_POLICY.md
    GITHUB_POLICY.md
    MEMORY_POLICY.md
    EXPLORATION_POLICY.md

  data/
    tasks/
      INBOX.md
      TASKS.md
      REVIEW.md
      DONE.md

    runs/
      2026-06-18/
        run-001.summary.md
        run-001.jsonl

    notes/
      README.md

    skills/
      README.md

    memory/
      hot/
        profile/
          user_preferences.md
          interest_map.yaml
        project/
          goals.md
          decisions.md
          open_questions.md
        skills/
        learnings/
      cold/
        archive/
        old_skills/
        old_runs/
        old_sources/
      proposals/
        memory/
        cooldown/

    exploration/
      raw/
      daily_reports/
      review_labels/
      preference_analysis/
      reuse_maps/

    proposals/
      rule_changes/
      resource_requests/
      project_candidates/

  state/
    heartbeat.json
    claims/
    locks/

  .github/
    CODEOWNERS
    ISSUE_TEMPLATE/
      agent_task.md
      exploration_program.md
    pull_request_template.md

  scripts/
    README.md
```

第一版不需要把所有文件都写满，但应先创建能让 agent 启动和协作的骨架：

- `rules/START_HERE.md`
- `rules/AGENT_PROTOCOL.md`
- `rules/PERMISSIONS.yaml`
- `rules/RESOURCE_APPROVALS.yaml`
- `rules/TASK_POLICY.md`
- `rules/GITHUB_POLICY.md`
- `data/tasks/`
- `data/runs/`
- `data/exploration/reuse_maps/`
- `data/proposals/rule_changes/`
- `.github/CODEOWNERS`
- `.github/ISSUE_TEMPLATE/`

## 12. MVP 实现顺序

### MVP 1：文件协议和单 worker tick

目标：

- 创建 rules / data / state 基础结构。
- 定义 rules/START_HERE.md，作为 Claude Code 空上下文启动入口。
- 定义 rules/AGENT_PROTOCOL.md。
- 创建 rules/PERMISSIONS.yaml 和 rules/RESOURCE_APPROVALS.yaml。
- 以 GitHub Issue 作为任务主入口。
- 用户本地手动启动 Code worker。
- 每次 tick 只处理一个任务。
- worker 必须 claim 一个 Issue，写入 lease 和 worker identity。
- tick 结束必须写 Issue comment、data/runs 和 data/tasks/REVIEW.md。
- worker 不得直接修改 rules/**，规则变更只能写入 data/proposals/rule_changes。

### MVP 1.5：GitHub 保护配置

目标：

- 创建 agent 独立 GitHub 账号，并赋予 repository write 权限。
- 人类账号保留 admin / owner 权限，负责审批和合并。
- 创建 .github/CODEOWNERS，指定 rules/** 和 .github/CODEOWNERS 归人类账号所有。
- 保护 main 分支，禁止直接 push，要求 PR 和 code owner review。
- 确认 agent 账号没有 admin 或 bypass branch protection 权限。

### MVP 2：任务队列和记忆沉淀

目标：

- GitHub Issue 自动同步到 data/tasks/TASKS.md 本地镜像。
- Issue label 和 TASKS 摘要保持状态流转一致。
- 运行结果写入 data/runs。
- 有 data/memory/proposals。
- reviewer 合并长期记忆到 data/memory/hot。
- 冷却 data/memory/hot 前必须进入 cooldown proposal 并通知用户。

### MVP 3：技能学习循环

目标：

- 用户写入技能名或链接。
- learner-worker 阅读、学习、跑 demo。
- 产出 data/memory/hot/skills/<skill>/SKILL.md 或 data/skills/<skill>/SKILL.md。
- 记录常见坑、命令、复用方式。
- Issue comment、run summary 或 skill note 中必须包含来源、整理笔记、实验证据和下一步建议。

### MVP 4：主动侦察

目标：

- 接入 GitHub / HN / arXiv / Product Hunt。
- 每日生成 scout report。
- 每天只推荐少量高价值行动。
- 每个长期方向先产出 existing work survey 和 reuse map。
- 记录 data/exploration/raw 和 daily_reports。
- 支持用户 review labels，并定期产出 preference_analysis。

### MVP 5：sandbox 实验执行

目标：

- 对高分项目自动 clone。
- 在隔离目录或容器中安装和运行。
- 记录失败原因和可修复方案。
- 生成下一步建议。

### MVP 6：多 worker 协同

目标：

- scout / learner / builder / reviewer 分工。
- claim / lock / lease 防冲突。
- 不同 worker 可以接力同一个长期目标。

## 13. 当前开放问题

- 每轮预算应该以 token、美元、时间还是任务数为主？
- 是否需要在第一版加入本地 hooks 检查 rules/** 写入，还是先只靠协议和 GitHub 保护？
- 是否需要 Docker sandbox，还是先用本地隔离目录？
- SQLite FTS 是否第一版就做，还是等记忆文件变多后再做？
- OpenViking / GBrain 是在 MVP 后试点，还是并行实验？
- GitHub Project 字段是否在第二阶段启用，还是长期只用 issue labels？
- 学习执行任务的输出是否需要固定模板，还是继续保持最低证据标准？
- 热区记忆降冷区的自动候选规则如何设置，例如 last_used_at、use_count、人工 pin？
- 是否启用 GitHub push rulesets 来进一步限制 rules/**，还是先只用 CODEOWNERS + branch protection？

## 14. 下一步建议

最小下一步：

```text
1. 创建 rules/START_HERE.md
2. 创建 rules/AGENT_PROTOCOL.md
3. 创建 rules/PERMISSIONS.yaml
4. 创建 rules/RESOURCE_APPROVALS.yaml
5. 创建 rules/TASK_POLICY.md
6. 创建 rules/GITHUB_POLICY.md
7. 创建 data/tasks/TASKS.md，作为 GitHub Issue 本地镜像
8. 创建 data/tasks/REVIEW.md
9. 创建 data/memory/hot 和 data/memory/cold 基础目录
10. 创建 data/proposals/rule_changes
11. 创建 .github/CODEOWNERS
12. 配置 main 分支保护和 required code owner review
13. 创建 GitHub Issue template
```

然后让本地 Code worker 执行第一条固定指令：

```text
Read rules/START_HERE.md and follow it exactly.
```
