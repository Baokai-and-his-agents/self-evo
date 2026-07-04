# Rule Change Proposal: Scout 稳定期治理层冻结

**日期:** 2026-07-04
**提案人:** refactor-worker-01
**对应审查:** docs/REFACTOR-direction-review.md Q1
**状态:** 待人类审批
**修改目标:** rules/AGENT_PROTOCOL.md(新增一节,不改现有内容)

## 背景

审查结论(Q1):治理层(rules 707 行 + scripts 护栏 2182 行)相对执行层(Scout Runner 刚刚交付)显得密集。但:

- 治理层成本是文件和行数,不是运行时开销
- 91+61+14 测试覆盖,精简反而引入回归风险
- blueprint v0.5 第 18 行明确"多 worker 协议要提前预留"

**因此不建议现在精简 rules**,而是建议**冻结扩张**——在 Scout 真实跑过 2 周前,不新增 rules 文件或扩充现有 rules。

## 建议修改

在 `rules/AGENT_PROTOCOL.md` 末尾新增一节:

```markdown
## Governance Freeze During Scout Stabilization (新增节)

在 Autonomous Scout 垂直切片完成并在真实来源上稳定运行 2 周之前:

- 不新增 rules/ 文件
- 不扩充现有 rules/ 文件的规则条目(修正笔误和事实错误除外)
- 任何新规则需求写入 data/proposals/rule_changes/,但不在本期内合并
- 本约束在 Scout 稳定 2 周后由人类评估是否解除

理由:治理层已超前于执行层。继续扩张治理而执行层未收口,会让治理失去现实校准——一个没被真实多 worker 压测过的协议可能藏着设计缺陷。冻结期内让 Scout 真实运行产生数据,再用数据决定治理层是否需要精简或扩张。
```

## 修改的规则项

- 文件: `rules/AGENT_PROTOCOL.md`
- 新增节: "Governance Freeze During Scout Stabilization"
- 不删除/修改任何现有内容

## 风险和回滚

**风险:** 低。冻结期是有期限的(Scout 稳定 2 周后评估),不是永久禁止。
**回滚:** 删除新增节即可。

## 相关证据

- docs/REFACTOR-evidence-pack.md 第 5 节(治理/执行量化)
- 审查报告 Q1 判断
- fx_backtest 闭环已证明协议可跑通(证据:8 claims, 47 commits)

## 明确反对的做法

- ❌ 现在精简 rules(测试覆盖好,精简是回归风险)
- ❌ 永久冻结治理(冻结是有期限的,目的是让数据说话)
- ❌ 解除冻结前合并新规则 proposal(包括本文件——本 proposal 也应等 Scout 稳定后才合并)
