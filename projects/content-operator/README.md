# Content Operator

`content-operator` 是 self-evo 下的内容生产业务项目。它把真实的 AI Agent
实践转化为可核验、可复盘、可持续迭代的内容资产。

## 当前目标

先跑通一条最小完整闭环：

```text
公开信息与真实项目证据
→ Agent 提供候选选题和理由
→ 人类选择
→ Agent 形成提纲与初稿
→ 事实核验和人工终审
→ 人工发布
→ 记录反馈并复盘
```

当前不是追求日更、流量或无人值守发布，而是验证 Agent 能否稳定辅助生产
有独特证据、有明确观点、能展示真实能力的内容。

## 内容定位

- 主主题：AI Agent 的真实实践、工作流、失败案例和复盘。
- 微信公众号：完整长文和品牌锚点。
- Twitter/X：短观点和表达实验；未获得单独授权前不访问账号或发布。
- self-evo：保存研究 brief、方法论、候选选题、运行记录和复盘证据。

## 决策边界

Agent 可以：

- 调研已批准的公开来源；
- 提供候选选题、证据、排序和风险；
- 起草提纲、初稿和平台改写版本；
- 执行事实核验并整理发布后数据。

必须由人类决定：

- 最终选题和核心观点；
- 是否接受提纲与终稿；
- 是否、何时、在哪个平台发布；
- 如何解释反馈并改变后续方向。

## 前五篇约束

前五篇内容保持人工发布。项目可以自动化调研、候选生成、草稿、核验和复盘，
但不得登录平台、点击发布、联系用户或使用私有数据。

完成五篇后，根据真实运行数据决定是否自动化排版、配图、排期或发布。

## 第一阶段

第一阶段执行 [`exploration/first-scout-brief.md`](exploration/first-scout-brief.md)：

1. 调研 20–30 个高质量公开样本；
2. 形成 AI Agent 内容方法论 v1；
3. 生成并排序 10 个候选选题；
4. Agent 推荐前三个，人类选择第一个。

方法论和选题分别使用：

- [`templates/methodology-v1.md`](templates/methodology-v1.md)
- [`templates/topic-candidates.md`](templates/topic-candidates.md)

## 下一次 Scout Run 的单入口指令

在为正式调研创建独立 GitHub Issue 并设置
`project:content-operator` 标签后，向 worker 提供：

```text
Read rules/START_HERE.md and follow it exactly. Claim the open
project:content-operator Scout issue that instructs you to execute
projects/content-operator/exploration/first-scout-brief.md. Do not access
private accounts or publish content.
```

正式调研必须使用新 Issue，不能继续占用项目初始化 Issue。

