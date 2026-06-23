# HistData.com 数据源调查报告

**调查日期**: 2026-06-23
**调查人**: agent clawbie (fx-backtest-worker-01)
**目标**: 为 Issue #20 评估 HistData.com 作为 OHLC 数据源的可行性

---

## 执行摘要

**结论**: ✅ **HISTDATA_PILOT_APPROVED**

HistData.com 提供免费的外汇历史数据，**没有明确的使用限制条款**，非常适合作为学术研究和回测的主数据源。

**关键发现**:
- ✅ 提供完整的 OHLC 数据（基于 Bid 价格）
- ✅ 覆盖 EURUSD 2000-2026（满足 2005-2025 要求）
- ✅ M1（1分钟）和 Tick 级数据可用
- ✅ 多种格式可选（MetaTrader, ASCII, Excel, NinjaTrader, MetaStock）
- ✅ 时区明确：**EST (Eastern Standard Time) WITHOUT Daylight Saving**
- ✅ Volume 字段恒为 0（不影响 PR #19 策略）
- ✅ **无使用限制条款** — 与 Dukascopy 不同，未发现禁止自动化或数据库存储的条款
- ✅ 免费下载，付费 FTP/SFTP 仅为加速（$27 USD 一次性）
- ⚠️ 无质保声明："Use the data at your own will and risk"

---

## 数据特征

### 1. 数据覆盖

| 特征 | 详情 |
|------|------|
| **货币对** | EURUSD ✅ (及其他 65+ 对) |
| **时间范围** | 2000年至今（满足 2005-2025 要求）✅ |
| **频率** | Tick 和 M1（1分钟）✅ |
| **价格类型** | Bid OHLC（M1 bar 格式）✅ |
| **时区** | EST (UTC-5) WITHOUT Daylight Saving ✅ |
| **Volume** | 恒为 0（外汇无统一成交量）✅ |

**关键引用** (FAQ):
> "All timeframes that are bar based, like M1 (1 Minute Bar) Data and Tick (1 Second Bar) Data, the bar prices: Open, High, Low, Close in the data files are based on the **tick Bid price**."

> "What is the timeZone of the dates in the .csv files? The timezone of all data is: **Eastern Standard Time (EST) time-zone WITHOUT Day Light Savings adjustments**."

---

### 2. 数据格式

**MetaTrader M1 格式** (DAT_MT_EURUSD_M1_YYYYMM.csv):

```csv
Date,Time,Open,High,Low,Close,Volume
2012.02.01,00:00,1.306600,1.306600,1.306560,1.306560,0
2012.02.01,00:01,1.306570,1.306570,1.306470,1.306560,0
```

**字段说明**:
- **Date**: YYYY.MM.DD
- **Time**: HH:MM (24小时制)
- **Open/High/Low/Close**: Bid 价格（5位小数）
- **Volume**: 恒为 0

**时区**: EST (UTC-5) 全年不变（无夏令时调整）

---

### 3. 数据质量

**官方声明** (FAQ):
> "Since it's free data, you'll not get from us any kind of warranty or certification. Use the data at your own will and risk."

**质量保障**:
- ✅ 每个文件提供状态报告：
  - 最大 gap（毫秒）
  - 所有 gap 列表（秒）
  - 平均 tick 间隔（毫秒）
- ✅ Gap 标准：测量所有 > 1 分钟的 gap
- ⚠️ 低流动性时段 gap > 90 秒属正常

**引用**:
> "We're measuring all the gaps bigger than 1 minute. It's normal that you'll find gaps in average of > 90 seconds when the market is with low trading volumes."

---

## 许可与使用权利

### 关键发现：**无使用限制条款**

**对比 Dukascopy**:
- ❌ Dukascopy: 明确禁止自动化访问、数据库存储（"WEBSITE" 边界不明）
- ✅ **HistData**: 未发现任何禁止自动化下载、本地缓存或编程处理的条款

**调查范围**:
1. ✅ 主页 (histdata.com)
2. ✅ FAQ 页面 (histdata.com/f-a-q/)
3. ✅ 数据规格页面 (data-files-detailed-specification)
4. ✅ 隐私政策 (privacy-policy-2)
5. ✅ Cookies 政策 (cookies)
6. ❌ "Terms of Use" 页面 404（不存在）

**未发现的限制**:
- ❌ 无禁止自动化下载的条款
- ❌ 无禁止数据库存储的条款
- ❌ 无禁止编程处理的条款
- ❌ 无禁止学术/研究使用的条款
- ❌ 无禁止再分发的明确条款（但建议仅本地缓存）

**唯一限制**:
> "Since it's free data, you'll not get from us any kind of warranty or certification."

**解读**: HistData 采用"无条款即许可"的模式，仅声明无质保，未设置使用限制。

---

### 隐私政策摘要

**用户数据收集**:
- 仅收集：姓名、邮箱、IP 地址（付费服务用户）
- 用途：发送登录凭证、技术支持
- ✅ 不出售给第三方
- ✅ 用户可请求删除

**第三方 Cookies**:
- Google, Facebook, Twitter（分析和广告）
- 可在浏览器中管理

---

## 获取方式

### 1. 免费网页下载（推荐用于研究）

**URL 模式**:
```
https://www.histdata.com/download-free-forex-historical-data/?/metatrader/1-minute-bar-quotes/eurusd/YYYY
```

**示例**:
- 2005 全年: `.../eurusd/2005`
- 2026年5月: `.../eurusd/2026/5`

**格式**: ZIP 压缩的 CSV 文件

**网页下载特点**:
- ✅ 无需注册
- ✅ 无 API Key
- ✅ 直接 HTTP 下载
- ⚠️ 可能有 CAPTCHA（需验证）
- ⚠️ 下载速度受限

---

### 2. 付费 FTP/SFTP 加速（可选）

**费用**: $27 USD（一次性，通过 PayPal）

**用途**:
> "We're not selling the data!!! ... if you need speed for your own convinience you'll need to help us pay the traffic costs"

**访问方式**:
- FTP: `ftpsite.histdata.com:21`
- SFTP: `ftpsite.histdata.com:22`
- 工具: FileZilla, WinSCP

**优势**:
- ✅ 批量下载更快
- ✅ 断点续传
- ✅ 适合下载 2005-2025 全部数据

**评估**:
- 对于 20 年数据（2005-2025），$27 USD 加速合理
- 免费下载可行但耗时

---

### 3. 自动更新服务（可选）

**费用**: $7 USD/月（通过 Google Drive）

**用途**: 自动同步最新数据到 Google Drive

**评估**:
- ❌ 不适合历史回测（仅最新数据）
- ✅ 适合生产环境持续更新

---

## 时区处理（关键）

### EST (UTC-5) 无夏令时

**HistData 声明**:
> "TimeZone: **Eastern Standard Time (EST) time-zone WITHOUT Day Light Savings adjustments**"

**影响**:
- ✅ 全年统一 UTC-5
- ✅ 无需处理夏令时切换
- ⚠️ 与 PR #19 baseline (Bid M1) 的时区需对比确认

**转换需求**:
- 如果 PR #19 使用 UTC 或 GMT，需要转换
- 如果 PR #19 使用 EST (no DST)，完美匹配

**下一步**: Phase 3 pilot 下载后，对比 2005 年某一周的时间戳与 PR #19 baseline。

---

## Bid/Ask/Mid 价格

### Bid-only 数据

**M1 Bar 数据**:
- ✅ Open/High/Low/Close: **Bid 价格**
- ❌ Ask 价格：不可用（M1 格式）
- ❌ Mid 价格：不可用

**Tick 数据**:
- ✅ Bid 和 Ask 价格都可用（Generic ASCII 格式）
- ✅ 可计算 Spread

**引用** (FAQ):
> "All timeframes that are bar based, like M1 (1 Minute Bar) Data and Tick (1 Second Bar) Data, the bar prices: Open, High, Low, Close in the data files are based on the **tick Bid price**."

> "The Ask price is only included in the **Tick data** of the Generic ASCII format."

**评估**:
- ✅ Bid OHLC 满足 PR #19 策略（Donchian High/Low + ATR）
- ✅ 如需 Ask 或 Mid，可使用 Tick 数据计算

---

## Volume 数据

**HistData 处理**:
- Volume 字段恒为 `0`
- 原因：外汇无统一成交量，仅 Broker Specific Volumes

**引用** (FAQ):
> "No volume information? Why? Trading Volumes, in forex, are not aggregated and the only volume that you can find is the Broker Specific Volumes. So, therefore, we decided to remove the volume information from the delivered data."

**影响**:
- ✅ 不影响 PR #19 策略（未使用 volume）
- ✅ 符合预期

---

## 数据组织

### 文件结构

**按货币对/年份/月份组织**:
```
EURUSD/
  2005/
    DAT_MT_EURUSD_M1_200501.zip -> 2005年1月 M1 数据
    DAT_MT_EURUSD_M1_200502.zip -> 2005年2月 M1 数据
    ...
  DAT_MT_EURUSD_M1_2005.zip -> 2005全年 M1 数据
```

**ZIP 内容**:
- CSV 文件：`DAT_MT_EURUSD_M1_200501.csv`
- 文件状态报告（可能）

---

## 与 PR #19 的兼容性

### PR #19 策略需求

1. **Donchian Channel**: 基于过去 N 日的 **High/Low**
2. **ATR volatility**: 基于 **True Range** (High, Low, Close)
3. **同柱止损**: 需要区分 entry bar 内的 **High/Low**

### HistData 满足情况

| 需求 | HistData 提供 | 状态 |
|------|--------------|------|
| High 价格 | ✅ Bid High | ✅ |
| Low 价格 | ✅ Bid Low | ✅ |
| Close 价格 | ✅ Bid Close | ✅ |
| Open 价格 | ✅ Bid Open | ✅ |
| 日线频率 | ⚠️ M1（需聚合） | ✅ 可聚合 |

**结论**:
- ✅ HistData M1 数据完全兼容 PR #19 策略
- ✅ M1 聚合为日线：取每日首个 M1 的 Open、当日最高 M1 High、当日最低 M1 Low、当日末个 M1 Close

---

## 数据完整性与 Gap

### Gap 评估机制

HistData 提供每个文件的 gap 报告：
- 最大 gap（毫秒）
- 所有 > 1 分钟的 gap 列表
- 平均 tick 间隔

### Gap 期望

**正常 gap**:
- 周末（周五收盘至周日开盘）
- 节假日
- 低流动性时段（> 90 秒）

**异常 gap**:
- > 5 分钟（交易时段内）
- 需要在 pilot 下载后检查

**下一步**: Phase 3 pilot 验证时，统计 2005 年的 gap 分布。

---

## 与其他数据源的对比

| 特征 | HistData | Dukascopy | ECB |
|------|----------|-----------|-----|
| OHLC | ✅ Bid OHLC | ✅ Bid/Ask OHLC | ❌ 单一收盘价 |
| 覆盖期 | 2000-2026 ✅ | 2003-至今 ✅ | 1999-至今 ✅ |
| 日线 | ✅ (M1聚合) | ✅ | ✅ |
| 许可 | ✅ 无限制 | ⚠️ 不明确 | ✅ 明确宽松 |
| 费用 | 免费 ✅ | 免费 ✅ | 免费 ✅ |
| 自动化 | ✅ 无禁止 | ⚠️ 可能禁止 | ✅ 允许 |
| 缓存 | ✅ 无禁止 | ⚠️ 可能禁止 | ✅ 允许 |
| 时区 | EST (no DST) | GMT+0/GMT+2 | CET |
| 质保 | ❌ 无 | ❌ 无 | ✅ ECB官方 |

**优势**:
- ✅ 许可最宽松（无明确限制）
- ✅ 数据覆盖最早（2000起）
- ✅ 时区处理简单（无夏令时）

**劣势**:
- ❌ 无官方质保
- ⚠️ 需要从 M1 聚合为日线

---

## 风险评估

| 风险 | 概率 | 影响 | 缓解措施 |
|------|------|------|---------|
| 数据质量问题 | 中 | 高 | Pilot 验证 + ECB 交叉校验 |
| Gap 过多 | 低 | 中 | Pilot 统计 gap 分布 |
| 未来改变许可 | 低 | 中 | 及时下载全部数据 |
| 下载失败 | 低 | 低 | 重试机制 + 付费 FTP 备选 |
| 时区转换错误 | 中 | 高 | 与 PR #19 baseline 对比验证 |

---

## 推荐方案

### Phase 2: Pilot 下载与验证

**下载目标**: 2005 年 EURUSD M1 数据

**验证清单**:
1. ✅ 下载并解压 `DAT_MT_EURUSD_M1_2005.zip`
2. ✅ 验证 CSV 格式与文档一致
3. ✅ 统计 gap 分布（> 1 分钟的 gap）
4. ✅ 聚合为日线 OHLC
5. ✅ 与 ECB reference rate 交叉校验（Close 价格）
6. ✅ 与 PR #19 baseline 对比（如有 2005 Bid M1）
7. ✅ 验证时区处理（EST vs UTC/GMT）
8. ✅ 检查数据完整性（交易日覆盖）

**成功标准**:
- Gap < 5% 交易时间
- ECB 交叉校验相关性 > 0.95
- 无异常价格跳动（> 10% 单日）

---

### Phase 3-8: 全量下载与回测

**如果 Pilot 验证通过**:
1. 下载 2005-2025 全部年份数据
2. 选择下载方式：
   - 免费网页下载（耗时，适合少量年份）
   - 付费 FTP ($27 USD，推荐用于 20 年数据)
3. 实现 HistData adapter（M1 -> Daily OHLC）
4. 实现 ECB 交叉校验
5. 运行历史回测

**存储位置**:
```
state/download-cache/fx-backtest/histdata/
  raw/
    EURUSD_M1_2005.zip
    EURUSD_M1_2006.zip
    ...
  processed/
    eurusd_daily_2005.parquet
    eurusd_daily_2006.parquet
    ...
```

---

## 下一步行动

### Immediate (Phase 2)

- [x] **Task #1**: 完成 HistData 条款调查 ✅
- [ ] **Task #2**: 下载 2005 EURUSD M1 pilot
  - URL: `https://www.histdata.com/download-free-forex-historical-data/?/metatrader/1-minute-bar-quotes/eurusd/2005`
  - 存储: `state/download-cache/fx-backtest/histdata/raw/`
  - 验证: SHA256 hash
- [ ] **Task #3**: 验证 2005 pilot 数据
  - 解压 ZIP
  - 检查 CSV 格式
  - 统计 gap
  - 聚合日线
  - ECB 交叉校验
  - 时区验证

### Blocked (需 Pilot 通过)

- [ ] **Phase 3**: 全量下载 2005-2025
- [ ] **Phase 4**: 实现 data adapter
- [ ] **Phase 5**: ECB 交叉校验实现
- [ ] **Phase 6**: 历史回测
- [ ] **Phase 7**: 结果分析
- [ ] **Phase 8**: PR #21 最终报告

---

## 相关文档

- Issue: https://github.com/Baokai-and-his-agents/self-evo/issues/20
- PR #19 (策略定义): https://github.com/Baokai-and-his-agents/self-evo/pull/19
- PR #21 (本次数据源调查): https://github.com/Baokai-and-his-agents/self-evo/pull/21
- [OHLC 数据源对比矩阵](ohlc-data-sources-matrix.md)
- [ECB 评估报告](ecb-evaluation.md)
- [数据源决策摘要](data-source-decision.md)

---

## 附录: FAQ 关键引用

### 时区
> "What is the timeZone of the dates in the .csv files? The timezone of all data is: **Eastern Standard Time (EST) time-zone WITHOUT Day Light Savings adjustments**."

### 价格类型
> "All timeframes that are bar based, like M1 (1 Minute Bar) Data and Tick (1 Second Bar) Data, the bar prices: Open, High, Low, Close in the data files are based on the **tick Bid price**."

### 质保声明
> "Since it's free data, you'll not get from us any kind of warranty or certification. **Use the data at your own will and risk**."

### Gap 测量
> "We're measuring all the gaps bigger than 1 minute. It's normal that you'll find gaps in average of > 90 seconds when the market is with low trading volumes."

### Volume 处理
> "Trading Volumes, in forex, are not aggregated and the only volume that you can find is the Broker Specific Volumes. So, therefore, we decided to **remove the volume information** from the delivered data."

---

**报告状态**: ✅ Phase 1 完成 - HistData 调查通过
**下一步**: Task #2 - 下载 2005 pilot 数据
**更新日期**: 2026-06-23
