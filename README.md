# F Stock · 全 AI 无人公司

基于热词 `f stock` 的可复现商业机会分析 + **Phase 0 信息站 Web 产品**（Vercel）。

选定模式：**公开市场情绪与投资者教育信息站（SEO + Ads + 事实提醒）**。否定未持牌投顾/买卖信号路径。一人 / 周≤20 小时 / 自有资金精益。

## Web 产品（`web/`）

**Production:** https://fstock-seven.vercel.app

Next.js App Router 站点：延迟行情、可复现 Market Pulse、教育内容、alerts waitlist。

```bash
cd web
npm install
npm test
npm run build
npm run dev
```

### 部署（Vercel）

- Root Directory: `web`
- 环境变量见 [`web/.env.example`](web/.env.example)
- Cron: 每日 `GET /api/cron/refresh`（需 `CRON_SECRET`）

```bash
cd web
npx vercel link --yes
npx vercel env add CRON_SECRET production
npx vercel --prod --yes
```

## 商业计划书复现

```bash
pip install -r requirements.txt
playwright install chromium

python scripts/verify_all.py      # 重算全部指标并自检
python scripts/build_html.py      # 生成 report/index.html
python scripts/export_pdf.py      # 生成 PDF
```

## 关键文件

| 路径 | 作用 |
|---|---|
| `web/` | 对外信息站（本迭代交付） |
| `scripts/assumptions.yaml` | BP 唯一假设入口 |
| `data/sources.json` | 外部数据出处 |
| `data/computed/*.json` | BP 计算结果 |
| `report/index.html` | 苹果视觉风格正式 BP 报告 |
| `report/FStock_Opportunity_Report.pdf` | 印刷级 PDF |
| `need.txt` | 原始输入（含已被证伪的旧数字） |

## Pulse 公式口径

```
z_ret  = five_day_return / stdev(last_60_daily_returns)
z_vol  = clip(today_volume / avg_volume_20 - 1, -3, 3)
s_news = clip(headline_polarity, -1, 1)
Pulse  = clip(50 + 15*z_ret + 10*z_vol + 10*s_news, 0, 100)
```

实现与单测：`web/lib/sentiment.ts`、`web/lib/sentiment.test.ts`。

## BP 回报公式口径

- 账面年化：`(1 + ROI5/100)^(1/5) - 1`
- 期望倍数：`EV = p·M_win + (1-p)·L`（L=0 亏光 / L=1 保本）
- 风险调整年化：`EV^(1/5) - 1`
- Kelly：`f* = p - (1-p)/b`；对 ¥1,000,000 池取半 Kelly，并受探针上限约束

## 免责声明

本仓库产出仅供商业研究与公共信息教育，**不构成证券投资建议或法律意见**。
