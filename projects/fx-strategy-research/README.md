# fx-strategy-research

self-evo 的首个业务项目：外汇量化策略研究。

本项目是 self-evo 这套「人类 + Agent 协作运营系统」**运营出来的业务产出**，与仓库顶层的运营方式（`rules/`、`scripts/`、`.github/`、`data/`）相分离。它通过 GitHub Issues #13 / #15 / #18 和 Draft PR #14 / #16 / #19 交付。

## 研究方向

围绕一个核心问题展开：

> 连续止损次数是否包含关于下一次趋势交易结果的信息？在相同交易信号和风险预算下，亏损后有限算术递增，是否优于固定仓位、确认后放大以及随机仓位映射？

四组对照策略（A/B/E/G）共享完全相同的 position-independent trade events，通过条件概率分析与置换检验验证因果关系。

## 目录结构

```text
projects/fx-strategy-research/
├── experiments/     # 可运行的回测代码（fx_backtest MVP：A/B/E/G 对照实验）
├── exploration/     # 研究过程的原始调研、日报和复用地图
│   ├── raw/
│   ├── daily_reports/
│   └── reuse_maps/
├── runs/            # 本项目的 run 摘要（按日期）
└── memory/          # 本项目沉淀的记忆（提案、决策）
```

## 关联

- 相关 Issues：#13（Phase A/B 研究）、#15（有限递增试探仓位）、#18（对照回测 MVP）
- 相关 PR：#14、#16、#19
- 任务的 `project: fx-strategy-research` 字段归属约定见 `data/tasks/TASKS.md`
- 运营方式与运营项目的分离方案见 Issue #29
