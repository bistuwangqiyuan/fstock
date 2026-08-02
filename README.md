# F Stock · 全 AI 无人公司商业机会报告

基于热词 `f stock` 的可复现商业机会分析：否定未持牌投顾/买卖信号路径，选定**公开市场情绪与投资者教育信息站（SEO + Ads + 事实提醒）**，按一人 / 周≤20 小时 / 自有资金精益约束建模。

## 快速复现

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
| `scripts/assumptions.yaml` | 唯一假设入口 |
| `data/sources.json` | 外部数据出处 |
| `data/computed/*.json` | 计算结果 |
| `report/index.html` | 苹果视觉风格正式报告 |
| `report/FStock_Opportunity_Report.pdf` | 印刷级 PDF |
| `need.txt` | 原始输入（含已被证伪的旧数字） |

## 公式口径

- 账面年化：`(1 + ROI5/100)^(1/5) - 1`
- 期望倍数：`EV = p·M_win + (1-p)·L`（L=0 亏光 / L=1 保本）
- 风险调整年化：`EV^(1/5) - 1`
- Kelly：`f* = p - (1-p)/b`；对 ¥1,000,000 池取半 Kelly，并受探针上限约束

## 免责声明

本仓库产出仅供商业研究与决策讨论，**不构成证券投资建议或法律意见**。
