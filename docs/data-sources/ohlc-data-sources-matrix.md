# OHLC 外汇数据源调查矩阵

**调查日期**: 2026-06-23  
**调查人**: agent clawbie  
**目标**: 为 Issue #20 寻找符合预注册协议的 OHLC 数据源

---

## 调查摘要

本文档对比多个外汇历史数据源，以找到符合以下要求的候选：
- ✅ 提供 OHLC 数据（支持 Donchian High/Low + ATR）
- ✅ 覆盖 EURUSD 2005-2025
- ✅ 日线频率
- ✅ 许可允许研究使用、本地缓存、可复现
- ✅ 可自动化下载或有明确获取流程

---

## 数据源对比矩阵

| 数据源 | OHLC | 覆盖期 | 日线 | 许可状态 | 费用 | 自动化 | 缓存 | 再分发 | 可复现性 |
|--------|------|--------|------|----------|------|--------|------|--------|----------|
| **Dukascopy** | ✅ | 2003+ | ✅ | ⚠️ 不明 | 免费 | ⚠️ 不明 | ⚠️ 不明 | ⚠️ 不明 | ⚠️ 待定 |
| **OANDA v20** | 待查 | 待查 | 待查 | 待查 | 待查 | 待查 | 待查 | 待查 | 待查 |
| **QuantConnect** | 待查 | 待查 | 待查 | 待查 | 待查 | 待查 | 待查 | 待查 | 待查 |
| **Yahoo Finance** | 待查 | 待查 | 待查 | 待查 | 待查 | 待查 | 待查 | 待查 | 待查 |
| **ECB** | ❌ | 1999+ | ✅ | ✅ 允许 | 免费 | ✅ | ✅ | ✅ | ✅ 高 |

**图例**:
- ✅ 明确支持 / 允许
- ❌ 不支持 / 禁止
- ⚠️ 不明确 / 需进一步调查
- 待查: 尚未调查

---

## 详细评估

### 1. Dukascopy Historical Data Export

**官方入口**: https://www.dukascopy.com/swiss/english/marketwatch/historical/

#### 数据特征
- **OHLC**: ✅ 提供 Bid OHLC / Ask OHLC
- **覆盖期**: 2003 年至今（满足 2005-2025 要求）
- **频率**: Tick / 1秒 / 1分 / 1小时 / **日线** ✅
- **品种**: EURUSD ✅
- **价格类型**: Bid / Ask（可交易价格）
- **精度**: Tick 级精度，可聚合为日线

#### 许可状态
**状态**: ⚠️ **DATA_TERMS_UNCLEAR**

**已调查** (2026-06-23):
- 网站通用 Terms of Use
- 发现禁止自动化访问"WEBSITE"（scraper, bot）
- 发现禁止将"WEBSITE"存储在数据库中

**未调查**:
- Historical Data Export 功能的专项条款
- JForex API 许可协议
- 账户内历史数据的使用边界

**不确定**:
- "WEBSITE"是否包括导出的 CSV 文件？
- "数据库"是否包括本地研究缓存？

**下一步**:
- [ ] 调查 Historical Data Export 页面是否有专项条款
- [ ] 调查 JForex API 文档中的许可说明
- [ ] 或联系 Dukascopy 获取明确说明

#### 获取方式
- **Web Export**: 手动通过网页导出 CSV
- **JForex API**: 可能支持程序化访问（需调查）
- **账户要求**: 似乎不需要（但需确认）

#### 评估
- ✅ 数据质量高（Tick 级原始数据）
- ✅ OHLC 完整
- ✅ 覆盖期充足
- ⚠️ 许可边界不明确
- ⚠️ 自动化下载合法性待定

**详见**: [dukascopy-terms-analysis.md](dukascopy-terms-analysis.md)

---

### 2. OANDA v20 REST API

**官方入口**: https://developer.oanda.com/

#### 数据特征（需调查）
- **OHLC**: 待确认
- **覆盖期**: 待确认
- **频率**: 待确认
- **品种**: 应支持 EURUSD
- **价格类型**: 待确认（Bid/Ask/Mid）

#### 许可状态
**状态**: 🔍 **待调查**

**需要调查**:
- [ ] OANDA API 许可条款
- [ ] 历史数据获取限制（时间范围、频率）
- [ ] 是否需要开立真实账户
- [ ] 是否需要账户余额或交易量
- [ ] 本地缓存是否允许
- [ ] 数据共享限制

#### 获取方式
- **REST API**: 程序化访问
- **账户要求**: 需要 OANDA 账户（待确认是否需要入金）
- **API Key**: 需要

#### 评估
- ⏳ 待调查

---

### 3. QuantConnect Forex Data

**官方入口**: https://www.quantconnect.com/data

#### 数据特征（需调查）
- **OHLC**: 待确认
- **覆盖期**: 待确认
- **频率**: 待确认
- **品种**: 应支持主要货币对
- **价格类型**: 待确认

#### 许可状态
**状态**: 🔍 **待调查**

**需要调查**:
- [ ] QuantConnect 数据许可
- [ ] 免费 tier 的限制
- [ ] 历史数据下载方式
- [ ] 本地缓存许可
- [ ] 是否可在 QuantConnect 平台外使用

#### 获取方式
- **QuantConnect API**: 可能需要在平台内使用
- **本地下载**: 待确认是否支持
- **账户要求**: 可能需要注册

#### 评估
- ⏳ 待调查

---

### 4. Yahoo Finance (yfinance)

**官方入口**: https://finance.yahoo.com/

#### 数据特征（需调查）
- **OHLC**: yfinance 通常提供 OHLC
- **覆盖期**: 需要确认 EURUSD 历史深度
- **频率**: 日线应该支持
- **品种**: 需要确认 EURUSD ticker（可能是 EURUSD=X）
- **价格类型**: 待确认

#### 许可状态
**状态**: 🔍 **待调查**

**需要调查**:
- [ ] Yahoo Finance Terms of Service
- [ ] yfinance 库的合法性（非官方库）
- [ ] 历史数据的完整性和可靠性
- [ ] 本地缓存限制

#### 获取方式
- **yfinance Python 库**: `pip install yfinance`
- **无账户要求**
- **示例代码**:
  ```python
  import yfinance as yf
  eurusd = yf.Ticker("EURUSD=X")
  hist = eurusd.history(start="2005-01-01", end="2025-12-31")
  ```

#### 评估
- ⏳ 待调查
- ⚠️ 数据质量和完整性需要验证

---

### 5. ECB USD/EUR Reference Rate

**状态**: ✅ **已调查完毕 - 仅用于交叉校验**

#### 数据特征
- **OHLC**: ❌ 仅单一收盘价
- **覆盖期**: ✅ 1999-至今（满足 2005-2025）
- **频率**: ✅ 日线
- **品种**: USD/EUR（需转换为 EURUSD）
- **价格类型**: Reference rate（2:15 pm CET）

#### 许可状态
**状态**: ✅ **明确允许**

- ✅ ECB Copyright Policy 允许研究使用
- ✅ 允许免费使用、复制、分发、修改
- ✅ 无自动化限制
- ✅ 无数据库存储限制
- ✅ 仅需引用来源

#### 用途
- ✅ 用于主数据源的 close 抽样交叉校验
- ❌ 不能作为主数据源（无 OHLC）

**详见**: [ecb-evaluation.md](ecb-evaluation.md)

---

## 推荐调查优先级

### 优先级 1: Dukascopy 专项条款澄清
**理由**:
- 数据质量最高（Tick 级原始数据）
- OHLC 完整，Bid/Ask 分离
- 历史覆盖充足
- 唯一障碍是许可不明确

**行动**:
1. 查找 Historical Data Export 页面的专项条款
2. 查找 JForex API 文档中的许可说明
3. 如果找不到，考虑联系 Dukascopy 支持

**预期时间**: 1-2 小时

---

### 优先级 2: OANDA v20 API 调查
**理由**:
- 官方 API，许可应该明确
- 作为经纪商，数据可靠性高
- 可能支持 OHLC 和 Bid/Ask

**行动**:
1. 阅读 OANDA API 文档
2. 确认历史数据获取方式
3. 确认许可条款
4. 测试 API 访问（如果可行）

**预期时间**: 2-3 小时

---

### 优先级 3: Yahoo Finance 快速验证
**理由**:
- 最快验证（可立即测试）
- 如果数据完整，可作为备选
- yfinance 库易于使用

**行动**:
1. 测试 EURUSD=X 数据可用性
2. 检查 2005-2025 覆盖
3. 验证 OHLC 完整性
4. 检查数据质量
5. 调查 Terms of Service

**预期时间**: 1 小时

---

### 优先级 4: QuantConnect
**理由**:
- 可能需要在平台内使用
- 可能不支持本地下载
- 作为最后备选

**行动**:
1. 阅读 QuantConnect 文档
2. 确认数据导出能力

**预期时间**: 1-2 小时

---

## 决策门槛

### 最低可接受标准

主数据源必须满足：
- ✅ 提供 OHLC 数据
- ✅ 覆盖 EURUSD 2005-2025
- ✅ 日线频率
- ✅ 许可明确允许研究使用
- ✅ 许可允许本地缓存
- ✅ 可复现（其他研究者可独立获取）
- ✅ 自动化下载或有清晰的手动流程

### 期望但非必需

- ✅ 免费或学术许可
- ✅ Bid/Ask 分离（而非仅 Mid）
- ✅ 官方 API（而非第三方库）
- ✅ 更长历史（如 2003+）

---

## 下一步行动

1. **Phase 1 继续**: 按优先级调查上述数据源
2. **生成详细评估**: 为每个数据源创建评估文档
3. **更新对比矩阵**: 填充"待查"字段
4. **提交人类决策**: 输出完整矩阵和推荐方案
5. **等待批准**: 在批准前不下载数据、不运行回测

---

## 相关文档

- [Dukascopy 调查报告](dukascopy-investigation.md)
- [Dukascopy Terms 分析](dukascopy-terms-analysis.md)
- [ECB 评估报告](ecb-evaluation.md)
- [数据源决策摘要](data-source-decision.md)

---

**当前状态**: 部分调查完成，需要补充 OANDA / QuantConnect / Yahoo Finance  
**下一步**: 优先澄清 Dukascopy 专项条款，并行测试 Yahoo Finance  
**目标**: 为人类提供完整的 OHLC 数据源对比和推荐方案
