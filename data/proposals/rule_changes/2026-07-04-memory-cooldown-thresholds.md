# Rule Change Proposal: 记忆冷却触发阈值

**日期:** 2026-07-04 (v2: 时效阈值 14→30 天,依据 Codex 定向复核)
**提案人:** refactor-worker-01
**对应审查:** docs/REFACTOR-direction-review.md Q3 + docs/REFACTOR-cooldown-recheck-by-codex.md
**状态:** 待人类审批
**修改目标:** rules/MEMORY_POLICY.md

## 背景

当前 MEMORY_POLICY.md 定义了 hot/cold/proposals 三层结构和冷却流程,但**没有规定何时触发冷却**。blueprint 第 1303 行把"冷却自动候选规则如何设置"列为开放问题。

现状:hot 7 + cold 5 + proposals 4 = 16 个记忆文件,冷却流程事实上不会运行,因为没有触发条件。

## 建议修改

在 `rules/MEMORY_POLICY.md` 的 "Cold Memory" 节之后,新增一节"冷却触发阈值":

```markdown
## Cooldown Triggers (新增节)

冷却流程在以下任一条件满足时启动候选生成(写入 `data/memory/proposals/cooldown/`):

- **规模触发:** hot 区文件总数超过 30 个
- **时效触发:** 单条记忆的 `last_referenced_at` 超过 30 天且未被 pin
- **强制触发:** hot 区文件总数超过 50 个时,必须启动一轮冷却提案

默认 pinned(不因时效自动冷却):
- `user_preferences` — 用户偏好
- `project/goals`、`project/decisions` — 项目目标和长期决策
时效冷却主要针对:非核心 learnings、旧 skills、临时研究结论。

阈值理由:
- 30 文件 = 人脑短期工作集规模上限,超过即认知负担
- 30 天 = self-evo 实际运行频率的合理周期。手动启动、单 worker、每次 tick 处理 0/1 任务,
  不是固定 sprint 节奏;14 天可能只是"这两周没轮到相关任务",30 天才更接近
  "跨过多个实际运行机会仍未被用到"
- 50 = 必须分类才能管理的规模,此时不冷却会失控

防堆积主要靠规模触发(hot>30 / >50),不是时间阈值——堆积是规模问题,该用规模阈值解决。
当前规模(16 文件)远未触发,这套机制属于"为增长预留",符合 blueprint 第 49 行
"复杂性由证据触发"——阈值本身不是复杂性,是让现有机制活起来的最小规则。
```

## 修改的规则项

- 文件: `rules/MEMORY_POLICY.md`
- 新增节: "Cooldown Triggers"
- 不删除/修改任何现有内容

## 风险和回滚

**风险:** 极低。只是给现有挂起的机制补触发条件,不改分层结构。
**回滚:** 删除新增节即可,无数据迁移。

## 相关证据

- docs/REFACTOR-evidence-pack.md 第 4 节(记忆文件数 16)
- blueprint 第 1303 行(开放问题)
- 审查报告 Q3 判断

## 不做的事

- ❌ 不改 hot/cold/proposals 三层结构(审查结论:结构合理)
- ❌ 不引入 SQLite FTS 或索引(blueprint 已正确延期)
- ❌ 不自动执行冷却,只生成候选(仍需人工审批,符合 MEMORY_POLICY 第 33-37 行)

## 修订记录

### v2 (2026-07-04): 时效阈值 14 天 → 30 天

v1 用 14 天,理由"sprint 周期"。经 Codex 定向复核(`docs/REFACTOR-cooldown-recheck-by-codex.md`)
裁决改 30 天,核心论据:

1. **self-evo 不是 sprint 节奏** — 手动启动、单 worker、tick 处理 0/1 任务,有流程但无固定周期;
   14 天可能只是"没轮到相关任务"
2. **堆积是规模问题,该用规模阈值解决** — 防堆积主要靠 hot>30 / >50,不该用时间阈值处理规模问题
3. **人工审批成本是稀缺资源** — 冷却需 proposal + 用户审批;短阈值 = 频繁打扰用户审低价值 proposal;
   self-evo 设计原则里人类带宽稀缺,应优先减少打扰
4. **核心记忆低频但关键** — 偏好/目标/决策常"低频但关键",两周没引用不代表该归档 → 补充默认 pinned 清单

14 天保留为"未来稳定每日/每周自动运行后"的重新评估候选,当前(手动启动阶段)不作为默认值。
