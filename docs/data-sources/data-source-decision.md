# Issue #20 数据源调查摘要

**调查日期**: 2026-06-23
**调查人**: agent clawbie
**Issue**: https://github.com/Baokai-and-his-agents/self-evo/issues/20

## 当前状态

⚠️ **HISTDATA_PILOT_REQUIRES_VALIDATION**

**更新**: 2026-06-23 晚间

Phase 1 已完成 HistData 2005 pilot 下载，但数据质量验证发现严重问题，必须完成验证才能批准全量下载：

1. **周末数据问题**: 315 个日期包含 50 个周日 + 7 个周六，共 ~15,924 个周末 M1 bars
2. **价格异常**: 2005-01-03 01:53 出现 ~90 pip 单分钟跳变，需要 ECB 交叉验证
3. **日线边界未定义**: Calendar day vs FX session 边界需要明确
4. **许可状态**: 应保持 DATA_TERMS_UNCLEAR（未找到明确条款 ≠ 获得许可）
5. **缓存文件**: 存在一个 31KB 损坏的 ZIP 文件需要清理

**当前阶段**: Phase 1 部分完成，暂停在 pilot 数据验证门
**下一步**: 完成周末数据分析、ECB 交叉验证、日线边界定义

---

## 调查结果摘要

### 1. Dukascopy Historical Data Export

**状态**: ⚠️ **DATA_TERMS_UNCLEAR**

**已调查**:
- 网站通用 Terms of Use
- 发现禁止自动化访问网站（scraper, bot）
- 发现禁止将"WEBSITE"存储在数据库中
- 仅限个人非商业使用

**未调查**:
- Historical Data Export 功能的专项条款
- JForex API 的许可协议
- 开立账户后下载历史数据的使用边界

**不确定的场景**:
- "WEBSITE"是否包括导出的 CSV 文件？
- "数据库"是否包括本地研究缓存？
- 手动导出后的文件是否可以编程处理？

**下一步**:
- 需要调查数据专项条款
- 或联系 Dukascopy 获取明确说明
- 或寻找替代 OHLC 数据源

**详见**: [dukascopy-terms-analysis.md](dukascopy-terms-analysis.md)

---

### 2. ECB USD/EUR Reference Rate

**状态**: ✅ **适合用于交叉校验**
**状态**: ❌ **不能作为主数据源**

**许可评估**:
- ✅ 许可明确且宽松（ECB Copyright Policy）
- ✅ 允许免费使用、复制、分发、修改
- ✅ 无自动化下载限制
- ✅ 无数据库存储限制
- ✅ 仅需引用来源

**数据特征**:
- 来源: European Central Bank
- 系列: EXR.D.USD.EUR.SP00.A
- 频率: 日线（每交易日 2:15 pm CET）
- 价格: Reference rate（单一收盘价）
- 覆盖: 1999-至今（满足 2005-2025 要求）

**关键限制**:
- ❌ 仅有单一收盘价，无 OHLC
- ❌ 无法支持 PR #19 的 Donchian High/Low + ATR 定义
- ❌ 改为 Close-based 策略违反 Issue #20 预注册协议

**用途**:
- ✅ 用于主数据源的 close 价格抽样交叉校验
- ✅ 检查方向、数量级、日期覆盖、异常点
- ❌ 不能作为主回测数据源

**详见**: [ecb-evaluation.md](ecb-evaluation.md)

---

## Issue #20 协议约束

### 策略定义已冻结

PR #19 已冻结策略定义：
- **Donchian Channel**: 基于过去 N 日的 **High/Low**
- **ATR volatility**: 基于 **True Range** (High, Low, Close)
- **同柱止损**: 需要区分 entry bar 内的 **High/Low**

Issue #20 明确禁止：
> "本轮不得搜索 entry period、exit period、ATR period、ATR multiplier、confirmation R 或 sizing 参数。若发现配置存在实现错误，只能修复错误，并说明修复前后；不得因为收益不佳而调整。"

**结论**: 将策略改为 Close breakout + Close volatility 属于**更换策略**，不是数据 adapter，违反预注册协议。

### 主数据源必须有 OHLC

Issue #20 明确：
> "ECB reference rate 不是可交易 OHLC，不能作为主回测数据；只用于方向、数量级、日期覆盖和异常点抽查。"

**结论**: 必须找到有 OHLC 的数据源，ECB 仅用于交叉校验。

---

## 下一步行动

### Phase 1 继续: 补充 OHLC 数据源调查

需要调查以下候选数据源，并对每项列出：
- OHLC / bid-ask 可用性
- 历史覆盖期（2005-2025）
- 日线 / 小时频率
- 账户 / API key 要求
- 费用（免费 / 付费）
- 自动化下载支持
- 本地缓存许可
- 再分发限制
- 可复现方式

#### 候选数据源

1. **Dukascopy**
   - 需要调查数据专项条款
   - Web Export / JForex API / 账户数据

2. **OANDA v20 API**
   - 官方文档: https://developer.oanda.com/
   - 需要调查历史数据获取方式和许可

3. **QuantConnect Forex Data**
   - 官方文档: https://www.quantconnect.com/data
   - 需要调查免费 tier 和许可

4. **Yahoo Finance (yfinance)**
   - Python 库: yfinance
   - 需要确认 EURUSD 数据可用性和 OHLC

5. **至少一个其他候选**
   - Quandl / Nasdaq Data Link
   - FRED (Federal Reserve)
   - 学术数据提供商
   - Interactive Brokers API

### Phase 1 输出

在完成 OHLC 数据源调查后，生成：
- OHLC 数据源对比矩阵（Markdown 表格）
- 每个数据源的详细评估文档
- 推荐方案和理由
- 提交给人类批准

### Phase 2-8 暂停

在人类批准主数据源前：
- ❌ 不下载数据
- ❌ 不实现下载器
- ❌ 不运行历史回测
- ❌ 不修改策略定义

---

## 交叉校验方案

无论选择哪个 OHLC 主数据源，使用 ECB reference rate 进行交叉校验：

### 校验内容
- 重叠日期数量
- Close 价格相关性
- 绝对差异分布（主数据 close - ECB rate）
- 相对差异分布（百分比）
- 最大异常日期识别

### 校验实施
```python
# data/adapters/ecb_cross_check.py
def cross_check_with_ecb(main_data_close, ecb_rate):
    """
    使用 ECB reference rate 对主数据源的 close 进行抽样检查

    Args:
        main_data_close: 主数据源的 close 价格
        ecb_rate: ECB USD/EUR reference rate

    Returns:
        cross_check_report: 包含相关性、差异分布、异常点
    """
    # 1. 对齐日期
    # 2. 转换货币对方向（如需要）
    # 3. 计算相关性
    # 4. 计算差异
    # 5. 识别异常点
```

---

## 风险与限制

### 已识别风险

| 风险 | 影响 | 缓解措施 | 状态 |
|------|------|---------|------|
| Dukascopy 许可不明 | 可能无法使用 | 调查专项条款或寻找替代 | ⏳ 进行中 |
| ECB 无 OHLC | 不能作为主数据源 | 仅用于交叉校验 | ✅ 已接受 |
| 策略定义已冻结 | 不能改为 Close-based | 必须找到 OHLC 数据源 | ⚠️ 约束 |
| 可能需要付费数据 | 增加成本 | 优先免费/学术许可数据 | ⏳ 待定 |

---

## 相关文档

- Issue: https://github.com/Baokai-and-his-agents/self-evo/issues/20
- PR #19: https://github.com/Baokai-and-his-agents/self-evo/pull/19
- [Dukascopy 调查报告](dukascopy-investigation.md)
- [Dukascopy Terms 分析](dukascopy-terms-analysis.md)
- [ECB 评估报告](ecb-evaluation.md)

---

**当前状态**: Phase 1 部分完成，需要补充 OHLC 数据源调查
**下一步**: 调查 OANDA v20、QuantConnect、Yahoo Finance 等 OHLC 数据源
**等待**: 人类批准主数据源或进一步调查指令
