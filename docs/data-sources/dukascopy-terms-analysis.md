# Dukascopy Terms of Use 分析报告

**分析日期**: 2026-06-23  
**分析人**: agent clawbie  
**文档来源**: https://www.dukascopy.com/swiss/english/legal-pages/terms-of-use/  
**分析目的**: 评估是否允许使用 Dukascopy 历史数据进行 Issue #20 的研究

## 执行摘要

**结论**: 🔴 **DATA_LICENSE_BLOCKED** - 有重大限制

Dukascopy Terms of Use 对数据使用施加了严格限制，特别是：
1. 仅允许个人非商业使用
2. 明确禁止自动化下载（scraper, bot, spider 等）
3. 禁止将数据存储在数据库中
4. 禁止再分发或与他人共享数据
5. 所有知识产权归 Dukascopy 所有

这些限制使得 Dukascopy 数据不适合用于本项目的可复现研究。

---

## 详细条款分析

### 1. 使用限制 (Section 3: Restrictions on Use)

#### 关键限制条款

> "you agree to use the WEBSITE solely for your own non-commercial use and benefit, and not for resale or other transfer or disposition to, or use by or for the benefit of, any other person or entity."

**影响**:
- ✅ 允许：个人非商业使用
- ❌ 禁止：为他人利益使用（包括开源项目）
- ❌ 禁止：转让或处置数据

> "You may not copy, reproduce, recompile, decompile, disassemble, reverse engineer, distribute, publish, display, perform, modify, upload to, create derivative works from, transmit, or in any way exploit any part of the WEBSITE"

**影响**:
- ✅ 允许：下载材料并打印一份副本（个人非商业用途）
- ❌ 禁止：复制、再分发、发布
- ❌ 禁止：上传到其他地方
- ❌ 禁止：创建衍生作品

> "The WEBSITE and the information contained therein may not be used to construct a database of any kind. Nor may the WEBSITE be stored (in its entirety or in any part) in databases for access by you or any third party"

**影响**:
- ❌ **明确禁止：构建任何类型的数据库**
- ❌ **明确禁止：将数据存储在数据库中**
- ❌ **明确禁止：为自己或第三方存储数据**

> "You may not use the WEBSITE in any way to improve the quality of any data sold or contributed by you to any third party."

**影响**:
- ❌ 禁止：使用数据改进任何要贡献给第三方的数据

#### 自动化限制

> "You shall not use or attempt to use any 'scraper,' 'robot,' 'bot,' 'spider,' 'data mining,' 'computer code,' or any other automate device, program, tool, algorithm, process or methodology to access, acquire, copy, or monitor any portion of the WEBSITE, any data or content found on or accessed through the WEBSITE, or any other WEBSITE information **without the prior express written consent of DUKASCOPY**."

**影响**:
- ❌ **明确禁止：任何自动化下载**
- ❌ 禁止：scraper, bot, spider, data mining
- ❌ 禁止：任何自动化程序、工具、算法
- ⚠️ **例外：需要 Dukascopy 明确书面同意**

### 2. 知识产权 (Section 2: Intellectual Property)

> "All present and future rights in and to trade secrets, patents, copyrights, trademarks, service marks, know-how, and other proprietary rights of any type under the laws of any governmental authority, domestic or foreign, including rights in and to all applications and registrations relating to the WEBSITE (the 'Intellectual Property Rights') shall, as between you and DUKASCOPY, at all times be and remain the sole and exclusive property of DUKASCOPY."

**影响**:
- 所有知识产权归 Dukascopy 独有
- 用户对数据没有所有权
- 用户只有有限的使用许可

### 3. 许可范围 (Section 4: License)

> "(i) You acquire absolutely no rights or licenses in or to the WEBSITE and materials contained within the WEBSITE other than the limited right to use the WEBSITE in accordance with the TCU. Should you choose to download content from the WEBSITE, you must do so in accordance with the TCU. Such download is licensed to you by DUKASCOPY ONLY for your own personal, non-commercial use in accordance with the TCU and does not transfer any other rights to you."

**影响**:
- 用户获得的是**极其有限的许可**
- 仅限个人非商业使用
- 不转移任何其他权利

### 4. 免责声明 (Section 7: Disclaimer)

> "the WEBSITE is provided for information purposes only"

> "none of the information contained on the WEBSITE constitutes a solicitation, offer, opinion, or recommendation by DUKASCOPY to use, buy or sell any security or other financial instrument or service"

**影响**:
- 数据仅供信息目的
- 不构成任何投资建议
- 不保证准确性、完整性、及时性

---

## 对 Issue #20 的具体影响

### 明确违反的条款

1. **数据库存储** (Section 3)
   - Issue #20 要求：将数据存储在 `state/download-cache/fx-backtest/`
   - Terms of Use: **明确禁止存储在数据库中**
   - 状态: ❌ **直接违反**

2. **自动化下载** (Section 3)
   - Issue #20 要求：实现可重复下载的 adapter
   - Terms of Use: **禁止任何自动化工具**（除非获得明确书面同意）
   - 状态: ❌ **直接违反**（除非获得书面授权）

3. **数据共享与复现** (Section 3)
   - Issue #20 要求：可复现的实验，包括数据来源
   - Terms of Use: 禁止为他人利益使用，禁止转让
   - 状态: ⚠️ **灰色地带**（如果其他研究者需要独立获取数据）

4. **派生作品** (Section 3)
   - Issue #20 要求：数据清洗、规范化、聚合
   - Terms of Use: 禁止创建衍生作品
   - 状态: ⚠️ **可能违反**（取决于如何解释"衍生作品"）

### 可能允许的使用

1. ✅ **手动下载用于个人研究**
   - 单次手动下载少量数据
   - 仅用于个人学习
   - 不存储在持久数据库

2. ✅ **查看在线数据**
   - 直接访问网站查看数据
   - 不下载和存储

---

## 风险评估

### 高风险

1. **法律风险**: 违反 Terms of Use 可能导致：
   - 终止访问权限 (Section 10)
   - 法律诉讼风险
   - 知识产权侵权索赔

2. **可复现性风险**:
   - 无法与其他研究者共享原始数据
   - 无法保证其他人能获得相同数据
   - 违背预注册研究的透明度原则

3. **实施风险**:
   - 需要手动下载（无自动化）
   - 无法构建可重复的数据管道
   - 无法满足 Issue #20 的技术要求

### 缓解措施（如果仍想使用 Dukascopy）

1. **获得明确书面许可**
   - 联系 Dukascopy 法务/合规部门
   - 说明研究目的（学术、非商业、开源）
   - 请求：
     - 允许自动化下载的书面授权
     - 允许存储数据的书面授权
     - 明确数据共享边界

2. **调整研究设计**
   - 仅使用 Dukascopy 作为交叉验证源（而非主数据源）
   - 使用其他具有明确研究许可的数据源
   - 记录无法使用 Dukascopy 的原因

3. **最小化风险使用**
   - 仅手动下载必要的小样本
   - 不构建自动化下载器
   - 不公开分享原始数据文件
   - 仅分享数据获取方法（让其他人自行下载）

---

## 替代方案

鉴于 Dukascopy 的严格限制，建议考虑以下替代数据源：

### 1. ECB (European Central Bank)
- **官方 API**: https://data.ecb.europa.eu/help/api/data
- **许可**: 通常允许研究使用
- **限制**: 仅有 reference rate，无 OHLC
- **建议**: 可作为主数据源（但需要接受无 OHLC 的限制）

### 2. Yahoo Finance
- **访问**: 通过 yfinance Python 库
- **许可**: 个人非商业使用
- **限制**: 历史深度有限，数据质量不确定
- **建议**: 适合快速原型，但需验证数据质量

### 3. FRED (Federal Reserve Economic Data)
- **官方 API**: https://fred.stlouisfed.org/
- **许可**: 公共领域数据
- **限制**: 主要是宏观经济数据，外汇数据有限
- **建议**: 可作为补充数据源

### 4. Quandl / Nasdaq Data Link
- **访问**: API 访问
- **许可**: 部分数据集允许研究使用
- **限制**: 需要验证具体数据集的许可
- **建议**: 值得调查

### 5. 学术数据提供商
- **例如**: Tick Data, Norgate Data, QuantQuote
- **许可**: 通常有明确的学术/研究许可
- **限制**: 可能需要付费
- **建议**: 如果预算允许，是最可靠的选择

---

## 建议

### 立即行动

1. ❌ **不要使用 Dukascopy 作为主数据源**
   - Terms of Use 限制太严格
   - 无法满足 Issue #20 的可复现性要求
   - 法律风险不可接受

2. ✅ **优先调查 ECB API**
   - 作为主数据源候选
   - 虽然只有 reference rate（无 OHLC），但许可明确
   - 可以调整研究设计以适应这一限制

3. ✅ **调查其他替代数据源**
   - Yahoo Finance (yfinance)
   - Quandl / Nasdaq Data Link
   - 学术数据提供商

4. ✅ **如果必须使用 Dukascopy**
   - 必须先获得明确书面许可
   - 联系方式: https://www.dukascopy.com/swiss/english/about/
   - 在获得授权前，不要开始下载

### 更新 Issue #20

建议在 Issue #20 中添加：
```markdown
## 数据源调查更新

### Dukascopy 评估结果
**状态**: ❌ DATA_LICENSE_BLOCKED

**原因**: Terms of Use 明确禁止：
- 自动化下载（需书面授权）
- 数据库存储
- 数据共享/转让

**决策**: 不使用 Dukascopy 作为主数据源

### 新数据源策略
1. 优先: ECB API (reference rate, 许可明确)
2. 备选: Yahoo Finance (yfinance)
3. 交叉验证: 保留 ECB 作为验证源
```

---

## 附录：关键条款原文

### 禁止数据库存储
> "The WEBSITE and the information contained therein may not be used to construct a database of any kind. Nor may the WEBSITE be stored (in its entirety or in any part) in databases for access by you or any third party or to distribute any database WEBSITEs containing all or part of the WEBSITE."

### 禁止自动化
> "You shall not use or attempt to use any 'scraper,' 'robot,' 'bot,' 'spider,' 'data mining,' 'computer code,' or any other automate device, program, tool, algorithm, process or methodology to access, acquire, copy, or monitor any portion of the WEBSITE, any data or content found on or accessed through the WEBSITE, or any other WEBSITE information without the prior express written consent of DUKASCOPY."

### 仅限个人非商业使用
> "you agree to use the WEBSITE solely for your own non-commercial use and benefit, and not for resale or other transfer or disposition to, or use by or for the benefit of, any other person or entity."

---

**最终建议**: 报告 `DATA_LICENSE_BLOCKED`，转向调查 ECB 或其他替代数据源。
