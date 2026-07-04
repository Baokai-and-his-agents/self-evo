# Scout Runner 复用地图
# Reuse Map for Autonomous Scout Runner

**日期:** 2026-07-04
**Worker:** refactor-worker-01
**触发:** 工作包 2a,落实 EXPLORATION_POLICY 第 7 行"先复用再自研"
**对应审查结论:** REFACTOR-direction-review.md Q2(抓取层复用、决策层自研)

---

## 设计前提(来自项目已有契约)

Scout Runner **不是从零设计**。以下契约已存在,runner 必须对接:

- `data/exploration/scout-source-registry.schema.yaml`(228 行 schema)
  - 4 种来源类型:web / api / rss / git
  - 4 种 cursor 策略:timestamp / item_id / etag / offset
  - 权限分层:public-web-read scope(read_public_pages / search_public_web / read_public_docs)
- `rules/RESOURCE_APPROVALS.yaml` 的 `public-web-read` 能力已批准
- blueprint 第 1000 行:输出是"决策流而非信息流"

**结论:runner 的接口边界已被项目自己的 schema 锁定。不需要新设计契约,只需要实现契约。**

---

## 可直接复用的成熟库(抓取层)

### 1. HTTP 抓取 → Python 标准库 + requests
- **来源:** Python stdlib `urllib` / `requests` 库(事实标准)
- **复用:** 所有 web/api 类型来源的 HTTP GET
- **适用:** schema 里 web 和 api 两种 type
- **理由:** 项目已用 Python 3(README 资源表),不引入新依赖
- **决策:** ✅ 采用 stdlib urllib(零新依赖);如需更友好的 API 用 requests(已在生态常见)

### 2. RSS/Atom 解析 → feedparser
- **来源:** [feedparser](https://github.com/kurtmckee/feedparser)(Python RSS 解析事实标准)
- **复用:** schema 里 rss type 的来源解析
- **适用:** 任何 RSS/Atom feed(博客 changelog、release notes)
- **注意:** feedparser 处理日期、编码、CDN 差异,自研会踩很多坑
- **决策:** ✅ 采用 feedparser(若引入依赖);否则用 stdlib xml.etree 解析 Atom(够用)

### 3. GitHub Trending / Search → GitHub REST API(via gh CLI 或 requests)
- **来源:** GitHub 官方 REST API + 已安装的 `gh` CLI(README 已列为推荐资源)
- **复用:** github-trending / github search 来源
- **适用:** schema example 里 github-trending
- **注意:** gh CLI 已在环境,优先用 `gh api`(免新依赖、自带 auth、遵守 rate limit)
- **决策:** ✅ 优先 `gh api`;无 gh 时 fallback 到 requests + anonymous(受 rate limit)

### 4. Hacker News → Firebase API(无需 token)
- **来源:** [HN Official API](https://github.com/HackerNews/API)
- **复用:** schema example 里 hacker-news(base_url 已是 firebase)
- **适用:** 公开只读,完全在 public-web-read scope 内
- **决策:** ✅ 直接 requests + JSON

### 5. arXiv → arXiv API(无需 token)
- **来源:** [arXiv API](https://info.arxiv.org/help/api/)
- **复用:** schema example 里 arxiv-cs-ai
- **适用:** Atom XML 格式,公开只读
- **决策:** ✅ stdlib xml.etree 解析 Atom

---

## 需要自研的部分(决策层)

### 决策层为何不能复用现成库

blueprint 第 1000-1008 行明确:"主动侦察的输出不应该是信息流,而应该是**决策流**"。现成 aggregator(如 RSS 阅读器、feedly 类)输出的是信息流(文章列表),**没有库能做"信息→3-5 个可执行决策"的转换**——这是 self-evo 的核心差异化。

### 自研模块清单

| 模块 | 职责 | 复用基础 |
|---|---|---|
| `decide/dedupe.py` | URL hash + mtime 去重 | 自研但极简(blueprint 第 49 行"复杂性由证据触发") |
| `decide/score.py` | 来源相关性打分 | 自研,对接 reuse map 格式 |
| `decide/report.py` | 生成决策流日报 | 复用 fx 的 run summary 模板形态 |

---

## 不建议使用 / 拒绝的方案

### ❌ 完整 ledger 系统(第一版)
- **原因:** blueprint 第 49 行"复杂性由证据触发";16 个文件不需要 ledger
- **替代:** 文件 mtime + URL hash 的最简去重
- **何时重评:** 去重 hash 文件超过 1000 条,或出现真实的"重复抓取浪费"

### ❌ 自研 HTTP/RSS 解析
- **原因:** 违背 EXPLORATION_POLICY 第 7 行"先复用再自研";HTTP/RSS 解析是已解决问题的重造轮子
- **替代:** stdlib + feedparser

### ❌ 第一版接入 Product Hunt API
- **原因:** schema 第 220 行已注明"PH API 需要 token,当前未批准"
- **替代:** 用 web 抓取(science 第 207-215 行 example 已示范)

### ❌ 引入 Scrapy /大型爬虫框架
- **原因:** 杀鸡用牛刀;单 worker 公开只读场景不需要分布式爬虫
- **替代:** requests + feedparser

---

## 推荐下一步

**直接采用:**
1. HTTP:stdlib urllib(零依赖)或 requests(若已在生态)
2. RSS:feedparser 或 stdlib xml.etree
3. GitHub:`gh api` 优先
4. HN/arXiv:requests + JSON/XML

**自研(不可避免):**
1. `decide/` 决策层——这是项目核心价值,无现成库
2. `cursor.py` 最简版——文件 mtime + URL hash

**先试用:**
- feedparser(若接受新依赖,RSS 解析最省事)
- 纯 stdlib(若想零依赖,xml.etree 解析 Atom 够用)

**继续调研:**
- 无。抓取层已确定复用方案,决策层已确定自研边界。

---

## 结论一句话

> Scout Runner 的实现策略:**抓取层全部复用(stdlib/requests/feedparser/gh api),决策层自研**。
> 这同时落实了 EXPLORATION_POLICY 的"先复用"原则和 blueprint 的"决策流"目标。
> runner 的接口边界已被项目自己的 schema 锁定,不需要新契约设计。
