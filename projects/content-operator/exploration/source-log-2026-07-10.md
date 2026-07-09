# Source Log — AI Agent 内容方法调研

**访问日期：** 2026-07-10  
**Run：** `2026-07-10-content-scout-001`  
**范围：** 25 个公开、无需登录的样本

## 搜索方法

共执行三轮搜索扩展：

1. 官方 Agent 工程指南、生产经验、评测与人工监督；
2. OpenAI、Anthropic、Google、Microsoft 等一手工程来源；
3. OpenAI 官方指南以及“何时不该用 Agent/为什么生产失败”的反方材料。

纳入标准：正文公开可读、作者或机构可识别、包含具体模式/案例/限制，或能作为
反例帮助判断内容可信度。社交登录墙、只有标题没有正文、纯聚合列表和页面失效的
结果被排除。

## 样本日志

| ID | 来源与 URL | 类型 | 选择理由 | 支持的结论 | 证据等级 |
|---|---|---|---|---|---|
| S01 | [Anthropic: Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) | 官方工程复盘 | 来自多团队实践，区分 workflow 与 agent | 简单可组合模式优先；先判断是否真的需要 Agent | 高 |
| S02 | [Anthropic: Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) | 官方方法指南 | 给出多轮 Agent 评测结构与部署经验 | 内容应解释测试方法、失败类型和生命周期，而不只展示 demo | 高 |
| S03 | [Anthropic: Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) | 官方方法指南 | 把上下文视为有限资源并给出清晰模型 | 好内容可围绕一个约束建立完整解释，而不是堆技巧 | 高 |
| S04 | [Anthropic: Writing effective tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents) | 官方工程指南 | 包含工具选择、命名空间、返回上下文和 token 效率 | 清单只有连接到评测和取舍时才有价值 | 高 |
| S05 | [Anthropic: How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) | 官方生产复盘 | 明确描述架构、收益、协调和可靠性挑战 | “How we built”应同时写设计理由、失败和边界 | 高 |
| S06 | [AWS: Evaluating AI agents](https://aws.amazon.com/blogs/machine-learning/evaluating-ai-agents-real-world-lessons-from-building-agentic-systems-at-amazon/) | 官方生产经验 | 聚焦 Amazon AgentCore 的真实评测经验 | 评测、可观测性和真实任务证据是 Agent 内容的可信度核心 | 高 |
| S07 | [LangChain: Building Better AI Agents](https://www.youtube.com/watch?v=reISMhbZ2XE) | 官方公开视频 | 以 trace、dataset、metric 串起可观测性和持续改进 | 视频/短内容也应给出可跟随的因果链和资源入口 | 中高 |
| S08 | [Maxim: AI Agent Evaluation — Top 5 Lessons](https://www.getmaxim.ai/articles/ai-agent-evaluation-top-5-lessons-for-building-production-ready-systems/) | 厂商方法文章 | 结构清晰，但同时销售自家产品 | 数字清单易读；厂商结论需要一手来源交叉验证 | 中 |
| S09 | [Monte Carlo: 10 Learnings After A Year](https://montecarlo.ai/blog-9-agentic-learnings-after-a-year-of-ai-deployment) | 厂商经验总结 | 用时间范围和客户/内部经验组织学习 | 标题中的时间和经验范围能建立上下文，但不等于独立证明 | 中 |
| S10 | [Galileo: Human-in-the-Loop Oversight](https://galileo.ai/blog/human-in-the-loop-agent-oversight) | 厂商实施指南 | 具体讨论生产 Agent 的人工监督 | 人类决策点必须落实到触发条件和责任，而非口号 | 中 |
| S11 | [Google: Long-running agents that pause and resume](https://developers.googleblog.com/build-long-running-ai-agents-that-pause-resume-and-never-lose-context-with-adk/) | 官方技术教程 | 以明确工程问题切入长任务状态管理 | 单问题深挖比宽泛的“Agent 大全”更可执行 | 高 |
| S12 | [Google: Agents CLI from create to production](https://developers.googleblog.com/agents-cli-in-agent-platform-create-to-production-in-one-cli/) | 官方产品教程 | 展示从创建到部署的一条完整路径 | 端到端内容应说明输入、步骤、产物和生产边界 | 中高 |
| S13 | [Google: Build multi-agent applications with ADK](https://developers.googleblog.com/en/agent-development-kit-easy-to-build-multi-agent-applications/) | 官方技术发布 | 以真实组件说明多 Agent 组合方式 | 发布类内容价值来自可运行示例，而不是能力口号 | 中高 |
| S14 | [Google: Agent2Agent Protocol](https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/) | 官方协议发布 | 解释互操作问题、设计目标和生态 | 新概念内容需要先说明旧问题和适用范围 | 高 |
| S15 | [Google: ADK integrations ecosystem](https://developers.googleblog.com/supercharge-your-ai-agents-adk-integrations-ecosystem/) | 官方生态发布 | 展示集成面，也带有推广属性 | 生态列表适合发现线索，不宜直接推导质量或采用建议 | 中 |
| S16 | [Google: Multi-agent patterns in ADK](https://developers.googleblog.com/developers-guide-to-multi-agent-patterns-in-adk/) | 官方模式指南 | 按模式、适用条件和实现组织内容 | “模式 + 何时使用 + 示例 + 限制”是强方法文章结构 | 高 |
| S17 | [Microsoft: Agent evaluation SDK](https://learn.microsoft.com/en-us/azure/foundry-classic/how-to/develop/agent-evaluate-sdk) | 官方文档 | 具体展示 Agent 评测接口和指标 | 方法文章应让读者能复现最小验证，而非只接受结论 | 高 |
| S18 | [Microsoft: CI/CD for AI Agents](https://techcommunity.microsoft.com/blog/educatordeveloperblog/cicd-for-ai-agents-on-microsoft-foundry/4522218) | 官方工程教程 | 把版本、质量门和环境晋升连成完整交付路径 | 可靠性主题适合用流程图和验收门讲清楚 | 中高 |
| S19 | [Microsoft: Three tiers of Agentic AI](https://techcommunity.microsoft.com/blog/azure-ai-foundry-blog/three-tiers-of-agentic-ai---and-when-to-use-none-of-them/4510377) | 官方观点/反方框架 | 明确讨论何时使用 workflow 或完全不用 Agent | 反直觉标题有效的前提是提供决策框架和反例 | 中高 |
| S20 | [Microsoft: Observability in generative AI](https://learn.microsoft.com/en-us/azure/foundry/concepts/observability) | 官方概念文档 | 定义 trace、evaluation、quality gate 和监控 | 权威定义适合作为背景，不足以单独形成独特文章 | 高 |
| S21 | [OpenAI: A practical guide to building agents](https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/) | 官方实践指南 | 从 use case、orchestration 到 guardrails 形成完整框架 | 实践指南应从适用任务开始，并把安全边界放入主流程 | 高 |
| S22 | [OpenAI: Identifying and scaling AI use cases](https://openai.com/business/guides-and-resources/identifying-and-scaling-ai-use-cases/) | 官方业务指南 | 关注从用例发现到规模化，但包含外部统计 | 统计必须追溯原始出处；业务价值不能只由采用率代替 | 中高 |
| S23 | [Sherlocks: Agent Failure Stack](https://www.sherlocks.ai/blog/why-ai-agents-fail-in-production) | 厂商失败分类 | 用分层框架解释静默失败与追踪难题 | 失败分类是好选题，但厂商数字和因果需独立核验 | 中 |
| S24 | [Towards Data Science: Built Backwards](https://towardsdatascience.com/most-ai-agents-fail-in-production-because-theyre-built-backwards/) | 二手观点 | 以强反直觉观点讨论从 Agent 而非问题出发的错误 | 可作为反方线索，不能单独支撑普遍失败率 | 低中 |
| S25 | [HackerNoon: Demos vs Production](https://hackernoon.com/why-ai-agents-work-in-demos-but-fail-in-production) | 二手观点 | 对 demo/生产差距做通俗表达 | 可学习问题 framing；结论必须回到官方或真实项目证据 | 低中 |

## 排除记录

- LinkedIn、Facebook 等登录墙结果：正文无法公开复核；
- GitHub “awesome”聚合列表：适合发现项目，不提供内容方法证据；
- 页面失效或仅有活动标题的结果：没有可用正文；
- 多个 SEO 型“最佳框架”页面：商业排序标准不透明；
- 无来源的增长数字与失败率：不进入核心结论。

## 证据边界

本样本主要来自官方工程博客、文档和厂商实践文章，能够支持“可信 Agent 实践内容
如何组织”的方法论；它不能支持微信公众号或 Twitter/X 的增长因果、最佳发布频率、
标题点击率或转化率结论。后者必须在本项目发布真实内容后另行验证。

