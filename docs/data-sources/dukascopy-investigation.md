# Dukascopy Historical Data 调查报告

**调查日期**: 2026-06-23  
**调查人**: agent clawbie  
**调查目的**: 评估 Dukascopy Historical Data Export 是否适合用于 Issue #20 的 EURUSD 回测研究

## 1. 数据源概况

### 官方入口
- **主页面**: https://www.dukascopy.com/swiss/english/marketwatch/historical/
- **提供方**: Dukascopy Bank SA (瑞士银行)
- **地址**: ICC, Entrance H, Route de Pré-Bois 20, 1215 Geneva 15, Switzerland
- **访问日期**: 2026-06-23

### 数据描述
根据官网页面描述：
- "The Historical Data Export provides historical price data for variety of financial instruments (e.g. Forex, Commodities and Indices)."
- 提供多种金融工具的历史价格数据，包括外汇、大宗商品和指数
- 数据格式：CSV
- 时间粒度：从 tick-by-tick 到月度数据
- 访问方式：通过 Historical Data Export 工具免费下载

### 数据获取方式
根据 FAQ 部分，有多种方式获取数据：
1. **网页工具**: Dukascopy Historical Data Export tool (免费)
2. **JForex 平台**: 登录 demo 或 live 版本，从菜单栏选择 Tools → Historical Data Manager
3. **MT4/MT5**: Tools → History Center

## 2. 使用条款初步调查

### 相关法律文档链接
- Terms of Use: https://www.dukascopy.com/swiss/english/legal-pages/terms-of-use/
- Privacy Policy: https://www.dukascopy.com/swiss/english/legal-pages/privacy-policy/
- Important Disclaimer: https://www.dukascopy.com/swiss/english/legal-pages/important-disclaimer/

### 免责声明要点（从页面底部提取）
- CFDs 是复杂工具，因杠杆作用具有快速亏损的高风险
- 74.94% 的零售客户账户在交易 CFD 时亏损
- 页面提到："All trading related information on the Dukascopy website is not intended to solicit residents of Belgium, Israel, Russian Federation, Turkey, Canada (including Québec) and the UK."
- 一般性声明：该网站不打算招揽访问者从事交易活动
- 警告：杠杆保证金交易和二元期权具有快速亏损的高风险

### 初步评估
**状态**: 🔴 **DATA_LICENSE_BLOCKED**

详细的 Terms of Use 分析显示 Dukascopy 施加了严格限制：
1. ❌ **明确禁止自动化下载**（需书面授权）
2. ❌ **明确禁止数据库存储**
3. ❌ **禁止数据共享/转让**
4. ✅ 仅允许：个人非商业手动下载单次使用

**结论**: Dukascopy 不适合作为 Issue #20 的主数据源。详见 `dukascopy-terms-analysis.md`。

## 3. 数据字段和价格类型

### 待确认事项
- [ ] 价格类型：bid / ask / mid / best bid/offer？
- [ ] OHLC 定义：基于什么时间边界？
- [ ] 时区：数据时间戳使用什么时区？
- [ ] 数据来源：是否为 Dukascopy 自身交易数据？
- [ ] 数据质量：是否经过清洗和验证？
- [ ] 企业行为：如何处理节假日、周末？

### 数据访问方式对比

| 方式 | 优点 | 缺点 | 适用场景 |
|------|------|------|---------|
| Web Export Tool | 无需账户，直接访问 | 手动操作 | 小量下载 |
| JForex API | 可编程，自定义时间范围 | 需要账户 | 批量下载 |
| MT4/MT5 | 熟悉的平台 | 有限的自定义 | 平台内使用 |

## 4. 覆盖范围评估

### 目标需求
- 品种：EURUSD
- 频率：日线（或从更低周期聚合）
- 时间范围：尽量覆盖 2005-01-01 至 2025-12-31

### 待验证
- [ ] Dukascopy 成立时间和数据起始日期
- [ ] EURUSD 数据是否完整覆盖目标区间
- [ ] 是否存在已知的数据缺口
- [ ] 日线数据是否可直接下载，还是需要从低周期聚合

## 5. 下一步行动

### 立即执行
1. ✅ 访问官方页面，记录基本信息
2. 🔄 详细阅读 Terms of Use
3. ⏳ 确认研究使用边界
4. ⏳ 查找数据字典和字段定义
5. ⏳ 测试数据下载接口

### 需要回答的关键问题
1. **许可问题**: 是否明确允许用于非商业研究？
2. **自动化问题**: 是否允许编程方式批量下载？
3. **再分发问题**: 下载的数据是否可以存储在本地？是否可以与其他研究者共享？
4. **归属要求**: 使用数据时是否需要标注来源？

### 风险评估
- 如果 Terms of Use 明确禁止研究使用或自动化下载 → 报告 `DATA_LICENSE_BLOCKED`
- 如果无法找到明确的使用边界说明 → 联系 Dukascopy 支持获取书面确认
- 如果许可模糊但无明确禁止 → 记录不确定性，谨慎使用并明确标注来源

## 6. 备用方案

如果 Dukascopy 不可用，考虑：
1. Yahoo Finance API (有限的历史深度)
2. FRED (Federal Reserve Economic Data)
3. ECB 作为主数据源（但不提供 OHLC）
4. 学术数据库（如 Quandl）

## 7. 记录保存

### 文档追踪
- 本文档: `docs/data-sources/dukascopy-investigation.md`
- 待创建: `docs/data-sources/dukascopy-terms-summary.md`
- 待创建: `docs/data-sources/dukascopy-data-dictionary.md`

### 下载记录模板
```
数据源: Dukascopy Historical Data Export
访问 URL: [具体 URL]
下载日期: YYYY-MM-DD
数据范围: YYYY-MM-DD 至 YYYY-MM-DD
文件名: [原始文件名]
SHA256: [校验和]
使用条款: [链接或摘要]
```

---

**状态**: 调查进行中  
**阻塞**: 需要完整阅读使用条款  
**下一步**: 获取并分析 Terms of Use 全文
