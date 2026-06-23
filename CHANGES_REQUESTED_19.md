# PR #19 变更请求

基于完整运行和代码审查，该 PR 完成了管道构建但存在多个会影响统计结论有效性的设计和实现缺陷。当前版本已通过所有测试并能成功运行 CLI 生成报告，输出显示 A 策略 +391.93%、E +979.83%，且 G 表明 B 的收益不具统计显著性。但这些数字存在问题。

要求修正：

1. **E 的仓位放大缺失或隐蔽**
`engine.py` 中找到传递 `in_confirmed_trend=True` 的地方，但 E 在真实确认前所有历史都是 `False`，意味着 sizing 永远看不到确认状态。正确做法是将确认时间戳嵌入 TradeEvent 本身的 entry/exit，或者更进一步：引入包含独立 confirmation timestamp/price 的不可变事件模型，并支持拆分计算 PnL，以便同一交易下先以 probe exposure 运行、确认后再按 amplified exposure 重算。当前实现要么不正确，要么过于隐蔽。需要人工构造的有真实 `r_confirmed` 的测试。

2. **G 的置换会截断事件流而非纯 sizing 标签置换作为 placebo**
当前 permutation 打乱 `0..K` 序列，这会将 K 本身置换到 0 的位置，导致第一次失败后提前终止所有后续事件。正确的做法是：G 应保持 B 所用的完整有效 event fraction multiset，只对有效 cycle budget 内的 sizing 标签置换，而不能把终止条件（K）放进置换逻辑。CLI 当前只用一个 seed=42，还应运行多个 seed placebo 计算分布，并报告 A/B/E 在 G 分布中的 percentile。需要验证 A/B/E/G 的 event IDs 是否完全相同、multiset 是否一致、不同 seed 是否可重现。

3. **B 的 cycle/budget 失败不连续**
policy 返回 0 导致 engine 内部 `break`，终止剩余事件。正确做法是：只有 cycle failure（K 次连败）、budget 用尽时才做 reset/cooldown 并继续后续 cycle。当前 budget 本身在 engine 内聚合，应该让 policy 返回 0 代表 event 内部暂停（这在当前设计可能难以表达），或重新设计使得明确区分有效止损序列、K、budget、reset 内部状态并继续。

4. **仓位换算为美元单位、美元单位换算错误**
`position_size = dollar_risk / price_distance` 给出 base currency units，而 `CostModel` 硬编码 standard lots 并假设 `$10/pip`，导致当前一笔 2 pip 交易可能输出成本 $4,225,012，明显是百万量级错误。需要明确定义 units 与 lots、pip size、contract size、quote/account currency。MVP 应聚焦只支持 EURUSD，非支持 pair 立即 fail closed。加入可手算验证成本测试，保证百万级量纲错误不再出现。

5. **统计结论存在过早断言和不充分样本下的定向结论**
报告多处呈现"consistently outperforms"等断言，n=1 CI 全部重叠 `all_overlap=True` 却仍做出定向结论。正确做法：预先设定最小样本要求（总体交易数、每 bucket n、placebo seed 数）并在不足时输出 `INSUFFICIENT_DATA`，禁止方向性结论。现有 Wilson CI 可保留；mean CI 需用正确 t 分位表或 bootstrap/exact 方法。

6. **缺失 Issue 要求的多项关键指标**
当前仅报告 expected log growth、volatility、downside deviation、CVaR/worst-tail、turnover、cost total、exposure/risk-budget utilization、cycle failure distribution。还需报告多个 seed G 分布及 B percentile。需要为所有指标编写可手算验证的测试。

7. **trade event 未验证 immutable**
`TradeEvent` dataclass 需加 frozen，并在每个测试前后对事件流做 hash/serialization before/after，证明所有 policy 从未修改事件。

8. **配置依赖非标准库**
`run.py` import `yaml`，PyYAML 不在标准库且 PR 说明声称零依赖。删除 PyYAML 及所有 YAML 文件，改为标准库（建议 JSON/TOML），若用 Python 内置 `tomllib`，则无外部配置依赖；如仍需配置文件，改 JSON。

9. **fixture 缺失对所有核心业务场景的确定性测试**
新增 deterministic fixture 替代或补充市场数据 fixture，覆盖止损序列、failure、reset、盈利、E confirmation、gap、成本。允许手算校验所有 event fixture；当前 synthetic fixture 只产出一笔结果仅可标为管道 smoke test，不应从单笔结果得出 stop_count 分桶平均的完整 cycle 测试。Fixture 应包含可重现至少一次 E confirmation、至少两次连续止损 K 次、reset、gap 超 stop、零成本与非成本场景、permutation 置换测试。

10. **命令行输出仅一次场景、未区分确定性测试结论 vs 真实数据阻塞**
当前一次运行未同时输出零与非零成本场景，也未在真实数据缺失时清晰输出 REAL_DATA_BLOCKED/INSUFFICIENT_DATA 级别告警。CLI 应一次运行 zero 和 conservative 两成本场景；输出机器可解析 JSON + 中文报告。没有真实数据时不应声称历史实证完成。

11. **任务生命周期文件不规范**
- canonical claim 应是 `state/claims/18.json`，当前自定义命名触发 validator `1 BLOCK/2 WARN`。
- heartbeat 当前混乱（多个文件），应只有 canonical `state/heartbeat.json`。Issue label 应是 `status:review`。
- `git diff --check` 当前报告尾随 trailing whitespace。
- PR 描述应描述真实实现与当前阻塞/限制，而非 validator/管道烟测。
- 清理所有运行产生的 output、`__pycache__` 临时文件并加入 .gitignore。

---

要求：逐项修正所有架构与业务正确性问题，并补充测试。MVP 不扩展到 C/D/F。优先级：1 事件模型与 A/B/E/G 内部正确性，2 成本与 reset 连续性，3 统计报告和 fixture 完备，4 生命周期规范。完成后分阶段 commit/push，中文 PR 评论。保持 Draft，不 Ready、不合并。
