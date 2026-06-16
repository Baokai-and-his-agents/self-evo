# 自学习和执行的自主 Agent 项目蓝图

日期：2026-06-16
状态：草案 v0.2

这个文件用于沉淀我们当前对“自学习和执行的自主 agent”的共识。后续所有设计调整、实现拆分、权限规则和记忆系统选择，都可以在这个文件基础上继续演化。

## 0. v0.2 已确认设计决策

v0.2 在 v0.1 的长期愿景上，先收敛第一版可测试系统：

- 第一版先做单 worker，用短周期 tick 验证学习和执行闭环。
- 任务入口以 GitHub Issue 为主；本地任务文件作为镜像、摘要和离线备份。
- 多 worker 不在第一版实际启用，但 Issue label、claim、lease、worker identity 和分支命名需要提前预留。
- 学习执行任务暂不固定笔记格式，但必须保留来源、整理笔记、实验或 demo 证据、可复用结论和下一步建议。
- 所有未明确授权的外部资源调用都需要用户确认；批准过的资源写入资源审批表，后续 worker 可按 scope 自动复用。
- 记忆默认进入热区；从热区降入冷区前必须通知用户，并允许用户要求调回热区。
- 主动探索可以适当发散，但每次探索必须留下轨迹，供用户后续 review 和偏好标注。

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

系统采用“文档通信 + Claude Code 长期执行 + supervisor 约束”的模式。

```text
用户
  ↓
文档协议
  ↓
Supervisor / Scheduler / Hooks
  ↓
一个或多个 Claude Code Worker
  ↓
学习、执行、实验、汇报、记忆更新
```

第一版用户主要通过 GitHub Issue 投递和追踪任务，同时通过本地文件沉淀长期记忆：

- 把任务、链接、技能名写入 GitHub Issue。
- agent 定时读取 open issue，claim 一个任务并执行。
- agent 把过程记录、阻塞点、需要确认的动作写回 issue comment 和本地 REVIEW。
- 用户可以通过 issue comment、label 或本地控制文件继续指导它。
- 本地 docs / memory 负责长期协议、运行摘要、技能沉淀和决策记录。

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

### 3.2 每次运行都必须可复盘

agent 每次 tick 都必须留下：

- 做了什么
- 为什么做
- 读了哪些资料
- 改了哪些文件
- 遇到哪些错误
- 哪些事情需要用户确认
- 哪些记忆建议写入长期记忆

不能只留下漂亮总结，必须保留足够证据。

### 3.3 主动性必须受控

agent 可以主动学习和探索，但不能无限浏览、无限总结、无限开新坑。

必须有：

- 任务预算
- 时间预算
- 成本预算
- 权限边界
- 每轮最多推进的任务数
- Review Queue

### 3.4 先低风险执行，再高风险确认

默认允许 agent 自动做以下低风险动作，但前提是没有触发未授权外部资源调用：

- 读取已批准范围内的公开资料
- 总结已批准范围内的链接
- 写本地笔记
- 创建本地 demo
- 在 sandbox 跑实验
- 生成计划和候选方案

默认需要用户确认：

- 所有未明确授权的外部资源调用
- 安装全局软件
- 改系统环境变量
- 使用私人账号
- 使用 API token 或私有凭证
- 使用服务器、云资源、GPU、付费模型或其它计算资源
- push 到远程仓库
- 创建 PR
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

### 3.5 资源审批表

所有外部资源授权都应记录在一个可审计的资源审批表中，建议路径：

```text
memory/profile/resource_approvals.yaml
```

worker 在使用任何外部资源前必须先查表：

1. 如果资源不存在、状态不是 approved、超出 scope、超出预算或已过期，写入 REVIEW 并等待用户确认。
2. 如果资源已批准，且本次用途在 scope 和 budget 内，可以自动使用。
3. token、密码、私钥等敏感值不能写入审批表，只能记录环境变量名、凭证来源说明或人工配置说明。
4. 每次使用外部资源后，需要在 run log 中记录资源 id、用途、估算成本和结果。

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
    approved_at: 2026-06-16
    notes: 只记录凭证引用，不记录 token 本身。
```

这个表会随着用户审批逐渐增长。第一阶段需要用户确认的事情会多一些；当常用资源都被明确授权后，worker 可以在边界内更自动地执行。

常见资源条目可以包括 `public-web-read`、`github-api-read`、`openai-api`、`cloud-vm`、`gpu-runtime` 等。公共网络读取也应作为资源被明确批准，而不是被隐含允许。

## 4. 文档通信协议

第一版任务主入口是 GitHub Issue。本地文档仍然重要，但职责更偏向协议、记忆和离线镜像。

建议建立如下目录：

```text
docs/
  AGENT_PROTOCOL.md        agent 行为协议
  CONTROL.md               用户当前总方向、偏好和禁区
  INBOX.md                 本地临时输入和离线备份，不是第一任务入口
  TASKS.md                 GitHub Issue 的本地镜像和摘要
  SKILLS.md                需要学习和训练的技能队列
  REVIEW.md                等待用户确认的事项
  DECISIONS.md             已确认的长期决策
  RUNLOG.md                agent 每轮执行摘要
  ARCHITECTURE.md          当前系统架构

state/
  heartbeat.json           worker 心跳
  locks/                   文件锁和任务锁
  claims/                  worker 对任务的认领记录
```

### 4.1 INBOX.md

用户可以随手写本地输入，不需要太结构化。第一版中，长期任务仍应优先创建为 GitHub Issue；INBOX 更适合临时草稿、离线输入或还没准备进入任务队列的想法。示例：

```md
## 2026-06-16

- 学习 Playwright browser automation
- 看这个项目是否值得做：https://example.com/project
- 研究 OpenViking 是否适合作为长期记忆后端
```

### 4.2 TASKS.md

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

### 4.3 REVIEW.md

agent 不能直接做的动作写入这里。示例：

```md
## R-20260616-001

task: T-20260616-001
request: 是否允许安装 Playwright 浏览器依赖？
risk: 会安装本地运行依赖，但不涉及系统账户或远程发布。
recommended_action: approve
```

### 4.4 学习执行任务最低证据标准

学习任务的输出形式不需要第一版定死，允许 worker 根据主题自行组织。但每个学习执行任务至少要留下：

- 原文链接、文档、仓库、论文或其它来源记录。
- 整理后的学习笔记，不能只保留原文摘录。
- worker 自己判断的重点、适用场景、限制和常见坑。
- 如果主题可执行，至少一个最小 demo、命令记录、实验结果或失败复现。
- 可进入长期记忆的候选条目。
- 下一步建议，包括继续深挖、转为构建任务、暂缓或归档。

这些内容可以写在 Issue comment、本地 run summary、memory proposals 或 skill note 中。验收先看证据是否足够支撑用户复审，后续再逐步沉淀更固定的格式。

## 5. GitHub 协调控制平面

v0.2 确认：第一版任务入口以 GitHub Issue 为主。GitHub 是人和 agent、多 agent 之间的共享状态协调层；本地文档是长期记忆和协议层。

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

worker 必须把 claim、阶段性进展、阻塞点、资源审批请求和完成摘要写回 Issue comment。涉及长期记忆的内容，再同步进入本地 memory proposals。

### 5.1 GitHub 对象映射

推荐映射：

```text
Issue
  一个可认领任务。

Label
  任务类型、权限等级、状态、worker 类型。

Assignee
  人类 owner，或代表某个 agent 的 GitHub bot/user。

Project
  看板视图，用于展示 backlog / claimed / in-progress / review / done。

Branch
  某个 agent 对某个任务的独立工作区。

Pull Request
  agent 的可审计输出和合并请求。

Issue comment
  agent 的进展日志、阻塞点、确认请求。
```

### 5.2 任务标签建议

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

### 5.3 防止两个 agent 做同一个任务

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

### 5.4 模块归属

多个 agent 可以长期负责不同模块，减少冲突：

```text
scout-worker
  labels: type:scout
  paths: memory/sources/**, memory/summaries/daily/**

learner-worker
  labels: type:learn
  paths: memory/skills/**, memory/learnings/**

builder-worker
  labels: type:build
  paths: app/**, scripts/**, tests/**

reviewer-worker
  labels: type:review
  paths: docs/REVIEW.md, memory/proposals/**, PR reviews
```

每个 worker 应该有默认可写路径。跨路径修改需要升级到 review 或人工确认。

### 5.5 PR 作为交付物

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

### 5.6 GitHub 与本地文档的关系

GitHub 是跨 agent 协调层，本地文档是项目记忆和执行协议层。

两边需要同步，但职责不同：

```text
GitHub Issues / Projects
  当前任务状态、所有权、PR、审计。

docs / memory
  长期设计、行为协议、技能、经验、决策、运行摘要。
```

同步规则：

- GitHub Issue 创建后，由 worker 或 supervisor 同步摘要到 docs/TASKS.md。
- 本地 INBOX.md 中的新任务，可以由 supervisor 转成 GitHub Issue；转完后写回 issue 链接。
- worker 的 claim、进展、阻塞、资源审批请求和完成摘要必须写入 Issue comment。
- 每次 tick 的本地证据、运行摘要和工具记录进入 docs/RUNLOG.md 与 memory/runs。
- 可复用技能、偏好、项目结论先进入 memory/proposals，review 后再合并到 hot memory。
- 重要长期决策进入 docs/DECISIONS.md 或 memory/hot/project/decisions.md。

### 5.7 适合使用 GitHub 的部分

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

这些仍然应留在本地 state、memory/runs 或专门的索引系统里。

## 6. Claude Code Worker 设计

第一版先运行单个 Claude Code worker，用短周期 tick 测试学习和执行闭环。不建议第一版让一个 Claude Code 会话永远不间断地跑。更稳的是用定时任务唤醒一个短周期 worker。

示例策略：

```text
每 30 分钟运行一次 tick
每次最多执行 1-2 个任务
每次有 max turns / max cost / max runtime
结束前必须写 Issue comment、RUNLOG 和 REVIEW
```

虽然第一版只启用一个 worker，但任务协议必须预留多 worker：

- 每次运行都带 worker identity，例如 `learner-worker-01`。
- 每个任务都走 claim / lease 流程，即使当前没有竞争。
- 分支命名使用 `agent/<worker>/<issue-number>-<slug>`。
- label 中保留 `agent:*`、`type:*`、`status:*` 和 `permission:*`。
- 本地 state/claims 和 Issue comment 都记录同一份 claim 信息。

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

Claude Code 本身负责思考和执行，但外层需要一个很薄的 supervisor 来约束它。

Supervisor 职责：

- 定时唤醒 worker
- 注入必要环境变量和 PATH
- 检查 Claude Code 是否能访问关键工具
- 控制每次运行预算
- 记录 worker 心跳
- 处理任务锁
- 检查输出是否符合协议

Hooks 职责：

```text
SessionStart
  加载 AGENT_PROTOCOL、检查环境、写 heartbeat。

PreToolUse
  拦截危险命令、越界路径、敏感文件读取、部署、付款、删除等动作。

PostToolUse
  记录命令、文件变化、失败信息。

Stop
  强制检查是否写入 RUNLOG、REVIEW、任务状态。

FileChanged
  对关键文档做格式检查和冲突检查。
```

特别注意：工具可用性不能只由外层 shell 判断。需要让 Claude Code worker 自己执行检查。Windows 上可能出现主 shell 能找到工具，但 Claude Code 子进程继承不到 PATH 的情况。

## 8. 记忆系统

记忆系统采用“文件为主、热冷分层、索引为辅、定期压缩、可人工纠偏”的设计。

```text
memory/
  profile/
    permissions.yaml
    resource_approvals.yaml

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

  tasks/
    inbox.md
    tasks.yaml
    review.md
    done.md

  runs/
    2026-06-16/
      tick-001.jsonl
      tick-001.summary.md

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
    permissions/

  exploration/
    raw/
    daily_reports/
    review_labels/
    preference_analysis/

  index/
    self_evo.sqlite
    embeddings/
```

### 8.1 热区和冷区

默认所有新长期记忆先进入热区。热区内容是 worker 启动和执行任务时可以优先读取的高频上下文。

冷区用于保存低频、过期、暂时不用但仍有保留价值的材料。冷区内容不能默认加载，需要通过检索、人工指定或探索任务进一步挖掘。

从热区转入冷区前，worker 必须：

1. 写入 memory/proposals/cooldown/*.md，说明候选条目、原因、最后使用时间和影响。
2. 在 REVIEW 或对应 GitHub Issue 中通知用户。
3. 等用户确认后再移动到 cold。

如果用户认为冷却不恰当，worker 应按用户意见把内容留在热区，或从 cold 调回 hot，并记录原因。

### 8.2 长期记忆写入规则

worker 不应直接随意改长期记忆。推荐流程：

```text
worker 观察和执行
  ↓
写 memory/proposals/*.md
  ↓
reviewer 或 supervisor 复核
  ↓
合并到 hot/profile、hot/project、hot/skills 或 hot/learnings
```

这样可以防止一次偶然失败被写成永久规则。

### 8.3 启动时加载上下文

每次 worker 启动时不应该加载全部记忆，而是按优先级加载：

```text
1. AGENT_PROTOCOL.md
2. permissions.yaml
3. hot/profile/user_preferences.md
4. hot/project/goals.md 和 hot/project/decisions.md
5. 当前任务
6. 相关 hot skill memory
7. 最近 1-3 次 run summary
8. 必要时检索 cold memory 或 index
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

v0.2 对探索的态度是：允许适当发散，但必须可复审。Token 和网络资源充裕时，可以扩大阅读和扫描范围；真正的约束不是“少看”，而是“看过什么、为什么看、为什么保留或丢弃”必须记录下来。

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
1 个最值得做的实验
1 个最值得学的技能
1 个最值得观察的商机
若干证据链接
```

每次探索还应留下探索轨迹：

```text
memory/exploration/raw/
  原始链接、查询词、API 返回摘要、保留和丢弃理由。

memory/exploration/daily_reports/
  每日探索摘要，突出值得继续看的内容。

memory/exploration/review_labels/
  用户 review 后的标注，例如 relevant、irrelevant、deep-dive、pause。

memory/exploration/preference_analysis/
  worker 对用户偏好的阶段性总结：为什么某些内容相关，为什么另一些偏题。
```

后续可以增加 preference learner：定期读取用户 review labels，总结主题边界、兴趣漂移和不相关模式，用来减少越学越散的问题。

## 10. 探索预算

主动 agent 必须有预算机制。v0.2 中预算不是为了压制探索，而是为了控制安全边界、资源上限和复盘粒度。由于用户允许较充裕的 token 和网络资源，探索预算可以相对宽松，但外部付费资源仍必须遵守资源审批表。

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

## 11. MVP 实现顺序

### MVP 1：文件协议和单 worker tick

目标：

- 创建 docs / memory / state 基础结构。
- 定义 AGENT_PROTOCOL。
- 创建 memory/profile/resource_approvals.yaml。
- 以 GitHub Issue 作为任务主入口。
- 用 Windows Task Scheduler 或脚本定时启动 Claude Code。
- 每次 tick 只处理一个任务。
- worker 必须 claim 一个 Issue，写入 lease 和 worker identity。
- tick 结束必须写 Issue comment、RUNLOG 和 REVIEW。

### MVP 2：任务队列和记忆沉淀

目标：

- GitHub Issue 自动同步到 TASKS 本地镜像。
- Issue label 和 TASKS 摘要保持状态流转一致。
- 运行结果写入 runs。
- 有 memory proposals。
- reviewer 合并长期记忆到 hot memory。
- 冷却 hot memory 前必须进入 cooldown proposal 并通知用户。

### MVP 3：技能学习循环

目标：

- 用户写入技能名或链接。
- learner-worker 阅读、学习、跑 demo。
- 产出 hot/skills/<skill>/SKILL.md。
- 记录常见坑、命令、复用方式。
- Issue comment、run summary 或 skill note 中必须包含来源、整理笔记、实验证据和下一步建议。

### MVP 4：主动侦察

目标：

- 接入 GitHub / HN / arXiv / Product Hunt。
- 每日生成 scout report。
- 每天只推荐少量高价值行动。
- 记录 memory/exploration/raw 和 daily_reports。
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

## 12. 当前开放问题

- Claude Code tick 的最佳运行频率是多少？
- 每轮预算应该以 token、美元、时间还是任务数为主？
- hooks 是否第一版就启用危险命令拦截？
- 是否需要 Docker sandbox，还是先用本地隔离目录？
- SQLite FTS 是否第一版就做，还是等记忆文件变多后再做？
- OpenViking / GBrain 是在 MVP 后试点，还是并行实验？
- 是否为每个 worker 创建独立 GitHub bot/user，还是用同一个账号加 worker identity comment？
- GitHub Project 字段是否在第二阶段启用，还是长期只用 issue labels？
- 学习执行任务的输出是否需要固定模板，还是继续保持最低证据标准？
- 热区记忆降冷区的自动候选规则如何设置，例如 last_used_at、use_count、人工 pin？

## 13. 下一步建议

最小下一步：

```text
1. 创建 docs/AGENT_PROTOCOL.md
2. 创建 docs/TASKS.md，作为 GitHub Issue 本地镜像
3. 创建 docs/REVIEW.md
4. 创建 memory/profile/permissions.yaml
5. 创建 memory/profile/resource_approvals.yaml
6. 创建 memory/hot 和 memory/cold 基础目录
7. 创建 scripts/tick.ps1
8. 创建 GitHub Issue template
```

然后让 Claude Code 执行第一条固定指令：

```text
Read docs/AGENT_PROTOCOL.md.
Read memory/profile/permissions.yaml and memory/profile/resource_approvals.yaml.
Find open GitHub Issues.
Claim exactly one open issue.
Execute only within the allowed permission level.
Write an Issue comment, docs/RUNLOG.md and docs/REVIEW.md before stopping.
```
