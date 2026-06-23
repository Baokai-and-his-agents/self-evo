# FX Position Sizing Backtest MVP

**Issue:** #18  
**Worker:** fx-backtest-worker-01  
**Run ID:** 2026-06-23-fx-backtest-001  
**Branch:** agent/fx-backtest-worker-01/18-fx-backtest-mvp

## 目的

实现 Issue #15 提出的四组仓位管理策略的离线回测对照实验：

- **A Fixed**: 固定风险重复试探
- **B Arithmetic-after-loss**: 止损后有上限的算术递增
- **E Confirm-then-amplify**: 固定小仓试探，独立趋势确认后一次性放大
- **G Placebo**: 保持交易结果序列不变，打乱 `stop_count/state -> size` 映射

## 核心研究问题

> 连续止损次数是否包含关于下一次趋势交易结果的信息？在完全相同的交易信号和风险预算下，亏损后有限算术递增是否优于固定仓位、确认后放大以及随机仓位映射？

## 关键约束

1. **统一事件流**: A/B/E/G 必须共享完全相同的 position-independent trade events
2. **无 lookahead**: 所有指标和信号只使用过去 bar
3. **可复现**: 固定 seed，确定性 fixture，记录所有配置
4. **条件概率分析**: `P(win|stop_count=n)`, `E[R|stop_count=n]` 及置信区间
5. **置换检验**: G 通过打乱 sizing-state 映射验证因果关系

## 目录结构

```
fx_backtest/
├── README.md                 # 本文件
├── run.py                    # 主 CLI 入口
├── configs/
│   └── mvp_daily.yaml       # MVP 预注册配置
├── fixtures/
│   └── deterministic.csv    # 小型测试数据
├── fx_backtest/             # Python 包
│   ├── __init__.py
│   ├── data.py              # 数据层
│   ├── signals.py           # 信号层
│   ├── engine.py            # 回测引擎
│   ├── sizing.py            # A/B/E/G 策略
│   ├── analysis.py          # 条件概率和统计
│   └── report.py            # 报告生成
└── tests/
    ├── test_data.py
    ├── test_signals.py
    ├── test_sizing.py
    └── test_engine.py
```

## 运行

```powershell
# 使用 fixture
python data/experiments/fx_backtest/run.py --config data/experiments/fx_backtest/configs/mvp_daily.yaml

# 真实数据（如果可用）
python data/experiments/fx_backtest/run.py --config data/experiments/fx_backtest/configs/mvp_daily.yaml --real-data
```

## 依赖

仅标准库，避免外部安装。如需扩展：
- 数据：CSV 格式，可选 pandas（若已安装）
- 统计：scipy（可选，用于置信区间计算）

## 状态

- [ ] 数据源调查
- [ ] 数据层实现
- [ ] 信号层实现
- [ ] 回测引擎实现
- [ ] Sizing policies 实现
- [ ] 条件概率分析实现
- [ ] 置换检验实现
- [ ] CLI 和报告生成
- [ ] 测试覆盖
- [ ] Fixture 运行
- [ ] 真实数据尝试
- [ ] 文档完成
