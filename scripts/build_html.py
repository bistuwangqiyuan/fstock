"""Build Apple-style report/index.html from data/computed/tables.json."""
from __future__ import annotations

import json
from pathlib import Path

from export_tables import main as export_tables
from lib_common import COMPUTED_DIR, ROOT

REPORT_DIR = ROOT / "report"


def fmt_cny(x: float) -> str:
    sign = "-" if x < 0 else ""
    return f"{sign}¥{abs(x):,.0f}"


def fmt_pct(x: float) -> str:
    return f"{x * 100:.2f}%"


def fmt_x(x: float) -> str:
    return f"{x:.2f}x"


def row_cls(x: float) -> str:
    if x < 0:
        return "neg"
    if x > 0:
        return "pos"
    return ""


def build(tables: dict) -> str:
    opp = tables["opportunity"]
    fin = tables["financials"]
    ret = tables["returns"]
    kelly = tables["kelly"]
    ue = tables["unit_economics"]
    phases = tables["phases"]
    sources = tables["sources"]["entries"]
    base_ret = ret["scenarios"]["base"]
    old = ret["old_need_audit"]
    selected = next(r for r in opp["rows"] if r["selected"])

    opp_rows_html = ""
    for r in opp["rows"]:
        star = "★" if r["selected"] else ""
        veto = f'<div class="muted small">否决：{r["veto_reason"]}</div>' if r.get("veto_reason") else ""
        opp_rows_html += f"""
        <tr class="{'selected' if r['selected'] else ''}">
          <td>{star} {r['name']}{veto}</td>
          <td>{r['scores']['compliance']:.1f}</td>
          <td>{r['scores']['solo_executable']:.1f}</td>
          <td>{r['scores']['capital_efficiency']:.1f}</td>
          <td>{r['scores']['automation']:.1f}</td>
          <td>{r['scores']['demand_reality']:.1f}</td>
          <td>{r['scores']['moat_realism']:.1f}</td>
          <td>{r['scores']['user_value_good']:.1f}</td>
          <td><strong>{r['weighted_score']:.2f}</strong></td>
        </tr>"""

    def fin_table(sc: str) -> str:
        block = fin["scenarios"][sc]
        body = ""
        for r in block["rows"]:
            body += f"""
            <tr>
              <td>Y{r['year_index']}</td>
              <td class="{row_cls(r['revenue_cny'])}">{fmt_cny(r['revenue_cny'])}</td>
              <td class="{row_cls(r['ebitda_cny'])}">{fmt_cny(r['ebitda_cny'])}</td>
              <td class="{row_cls(r['cumulative_ebitda_cny'])}">{fmt_cny(r['cumulative_ebitda_cny'])}</td>
              <td>{r['book_roi_pct']}%</td>
            </tr>"""
        pb = block["payback_vs_risk_capital_year"] or "未回本"
        return f"""
        <div class="card-block">
          <h4>{sc} · 风险本金 {fmt_cny(block['risk_capital_cny'])} · 回本 {pb}</h4>
          <table>
            <thead><tr><th>年</th><th>营收</th><th>EBITDA</th><th>累计EBITDA</th><th>账面ROI路径</th></tr></thead>
            <tbody>{body}</tbody>
          </table>
        </div>"""

    fin_html = "".join(fin_table(sc) for sc in ["conservative", "base", "optimistic"])

    ret_rows = ""
    for sc, b in ret["scenarios"].items():
        ret_rows += f"""
        <tr>
          <td>{sc}</td>
          <td>{fmt_pct(b['win_prob'])}</td>
          <td>{fmt_x(b['payoff_ratio_b'])}</td>
          <td>{fmt_x(b['m_win'])}</td>
          <td>{fmt_pct(b['book']['r_book'])}</td>
          <td>{fmt_x(b['ev']['ev_l0'])} / {fmt_x(b['ev']['ev_l1'])}</td>
          <td>{fmt_pct(b['ev']['r_risk_l0'])} / {fmt_pct(b['ev']['r_risk_l1'])}</td>
        </tr>"""

    kelly_rows = ""
    for sc, b in kelly["scenarios"].items():
        kelly_rows += f"""
        <tr>
          <td>{sc}</td>
          <td>{fmt_pct(b['p'])}</td>
          <td>{b['b']:.2f}</td>
          <td class="{row_cls(b['f_star'])}">{fmt_pct(b['f_star'])}</td>
          <td>{fmt_pct(b['half_kelly'])}</td>
          <td>{fmt_cny(b['recommended_deploy_cny'])}</td>
        </tr>"""

    phase_html = ""
    for key in ["phase0", "phase1", "phase2"]:
        ph = phases[key]
        goals = "".join(f"<li>{g}</li>" for g in ph["goals"])
        crit = "".join(f"<li>{c}</li>" for c in ph["pass_criteria"])
        phase_html += f"""
        <div class="phase">
          <h4>{ph['name']}</h4>
          <div class="two-col">
            <div><div class="label">阶段目标</div><ul>{goals}</ul></div>
            <div><div class="label">可检验标准</div><ul>{crit}</ul></div>
          </div>
        </div>"""

    sources_html = "".join(
        f"""
        <tr>
          <td>{s['field']}</td>
          <td>{s['value']}</td>
          <td class="small"><a href="{s['url']}">{s['url']}</a></td>
          <td class="small">{s.get('notes','')}</td>
        </tr>"""
        for s in sources
    )

    base_rev = [r["revenue_cny"] for r in fin["scenarios"]["base"]["rows"]]
    max_rev = max(base_rev) or 1
    bars = ""
    for i, v in enumerate(base_rev, 1):
        h = max(8, int(140 * v / max_rev))
        bars += f"""
        <div class="bar-col">
          <div class="bar" style="height:{h}px"></div>
          <div class="bar-val">{fmt_cny(v)}</div>
          <div class="bar-lbl">Y{i}</div>
        </div>"""

    old_y1 = fin["contrast_old_need"]["old_y1_to_y5_revenue_cny"][0]
    kelly_note = (
        "基准情景下 Kelly 为负，说明按二元赔率不应扩张风险本金；"
        "仅保留信息期权级探针，用阶段关卡决定加注或止损。"
        if kelly["scenarios"]["base"]["f_star"] <= 0
        else "基准情景半Kelly为正，但仍受探针上限约束；禁止全仓。"
    )

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{tables['meta']['title']}</title>
<link rel="stylesheet" href="print.css" />
<style>
:root {{
  --bg: #f5f5f7;
  --surface: #ffffff;
  --ink: #1d1d1f;
  --secondary: #6e6e73;
  --line: rgba(0,0,0,0.08);
  --accent: #0071e3;
  --accent-soft: rgba(0,113,227,0.08);
  --neg: #b91c1c;
  --pos: #0f766e;
  --shadow: 0 20px 60px rgba(0,0,0,0.06);
}}
* {{ box-sizing: border-box; }}
html {{ scroll-behavior: smooth; }}
body {{
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "SF Pro Text",
    "PingFang SC", "Helvetica Neue", sans-serif;
  color: var(--ink);
  background:
    radial-gradient(1200px 600px at 10% -10%, #e8eef8 0%, transparent 55%),
    radial-gradient(900px 500px at 100% 0%, #f0f4fa 0%, transparent 50%),
    var(--bg);
  line-height: 1.55;
  -webkit-font-smoothing: antialiased;
}}
.wrap {{ max-width: 980px; margin: 0 auto; padding: 48px 28px 96px; }}
.hero {{
  min-height: 86vh;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  padding: 48px 0 64px;
  border-bottom: 1px solid var(--line);
  animation: rise 0.9s ease both;
}}
.brand {{
  font-size: clamp(40px, 7vw, 72px);
  font-weight: 700;
  letter-spacing: -0.035em;
  line-height: 1.05;
  margin: 0 0 18px;
}}
.lede {{
  font-size: 21px;
  color: var(--secondary);
  max-width: 34em;
  margin: 0 0 28px;
}}
.meta-row {{
  display: flex; flex-wrap: wrap; gap: 10px 18px;
  font-size: 13px; color: var(--secondary);
}}
.pill {{
  display: inline-flex; align-items: center; gap: 8px;
  padding: 6px 12px; border-radius: 999px;
  background: var(--surface); border: 1px solid var(--line);
}}
.dot {{ width: 7px; height: 7px; border-radius: 50%; background: var(--accent); }}
section {{
  padding: 64px 0 24px;
  border-bottom: 1px solid var(--line);
  animation: rise 0.8s ease both;
}}
section:last-of-type {{ border-bottom: 0; }}
h2 {{
  font-size: 34px; letter-spacing: -0.03em; margin: 0 0 12px; font-weight: 700;
}}
h3 {{ font-size: 22px; letter-spacing: -0.02em; margin: 36px 0 12px; }}
h4 {{ font-size: 17px; margin: 0 0 12px; }}
.section-lede {{ color: var(--secondary); font-size: 17px; max-width: 46em; margin: 0 0 28px; }}
.metrics {{
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 14px;
  margin: 28px 0;
}}
.metric {{
  background: var(--surface);
  border: 1px solid var(--line);
  border-radius: 18px;
  padding: 18px 16px;
  box-shadow: var(--shadow);
}}
.metric .k {{ font-size: 12px; color: var(--secondary); margin-bottom: 8px; }}
.metric .v {{ font-size: 26px; font-weight: 650; letter-spacing: -0.03em; }}
.metric .s {{ font-size: 12px; color: var(--secondary); margin-top: 6px; }}
.callout {{
  background: var(--accent-soft);
  border: 1px solid rgba(0,113,227,0.15);
  border-radius: 18px;
  padding: 18px 20px;
  margin: 18px 0 28px;
}}
.warn {{
  background: #fff7ed;
  border: 1px solid #fed7aa;
  border-radius: 18px;
  padding: 18px 20px;
  margin: 18px 0 28px;
}}
.danger {{
  background: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: 18px;
  padding: 18px 20px;
  margin: 18px 0 28px;
}}
table {{
  width: 100%;
  border-collapse: collapse;
  background: var(--surface);
  border: 1px solid var(--line);
  border-radius: 16px;
  overflow: hidden;
  font-size: 13px;
}}
th, td {{
  padding: 12px 10px;
  text-align: left;
  border-bottom: 1px solid var(--line);
  vertical-align: top;
}}
th {{
  background: #fafafa;
  font-weight: 600;
  color: var(--secondary);
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}}
tr.selected td {{ background: rgba(0,113,227,0.05); }}
tr:last-child td {{ border-bottom: 0; }}
.neg {{ color: var(--neg); }}
.pos {{ color: var(--pos); }}
.muted {{ color: var(--secondary); }}
.small {{ font-size: 12px; }}
.card-block {{
  background: var(--surface);
  border: 1px solid var(--line);
  border-radius: 18px;
  padding: 18px;
  margin: 0 0 16px;
  box-shadow: var(--shadow);
}}
.two-col {{
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 18px;
}}
.label {{ font-size: 12px; color: var(--secondary); margin-bottom: 6px; font-weight: 600; }}
ul {{ margin: 0; padding-left: 1.1em; }}
li {{ margin: 6px 0; }}
.bars {{
  display: flex; align-items: flex-end; gap: 18px; height: 200px;
  padding: 24px 8px 8px; margin: 12px 0 28px;
}}
.bar-col {{ flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: flex-end; }}
.bar {{
  width: 100%; max-width: 72px;
  background: linear-gradient(180deg, #2f7cf6, #0071e3);
  border-radius: 10px 10px 4px 4px;
  animation: grow 1s ease both;
}}
.bar-val {{ font-size: 11px; margin-top: 8px; color: var(--secondary); }}
.bar-lbl {{ font-size: 12px; font-weight: 600; margin-top: 2px; }}
.phase {{
  background: var(--surface);
  border: 1px solid var(--line);
  border-radius: 18px;
  padding: 20px;
  margin-bottom: 14px;
}}
.flow {{
  display: flex; flex-wrap: wrap; gap: 8px; align-items: center;
  margin: 20px 0 28px; font-size: 13px;
}}
.flow span {{
  background: var(--surface);
  border: 1px solid var(--line);
  padding: 8px 12px;
  border-radius: 999px;
}}
.flow .arrow {{ border: 0; background: transparent; color: var(--secondary); padding: 0 2px; }}
.code {{
  font-family: "SF Mono", ui-monospace, Menlo, Consolas, monospace;
  font-size: 12px;
  background: #1d1d1f;
  color: #f5f5f7;
  border-radius: 14px;
  padding: 16px 18px;
  overflow-x: auto;
}}
.footer {{
  margin-top: 48px;
  padding-top: 24px;
  color: var(--secondary);
  font-size: 12px;
}}
a {{ color: var(--accent); text-decoration: none; }}
a:hover {{ text-decoration: underline; }}
@keyframes rise {{
  from {{ opacity: 0; transform: translateY(12px); }}
  to {{ opacity: 1; transform: none; }}
}}
@keyframes grow {{
  from {{ transform: scaleY(0.2); transform-origin: bottom; opacity: 0.3; }}
  to {{ transform: none; opacity: 1; }}
}}
@media (max-width: 820px) {{
  .metrics {{ grid-template-columns: 1fr 1fr; }}
  .two-col {{ grid-template-columns: 1fr; }}
  .brand {{ font-size: 40px; }}
  table {{ display: block; overflow-x: auto; }}
}}
</style>
</head>
<body>
<main class="wrap">
  <header class="hero">
    <div class="pill"><span class="dot"></span>全 AI 无人公司 · 自有资金精益 · v{tables['meta']['version']}</div>
    <h1 class="brand">F Stock</h1>
    <p class="lede">公开市场情绪与投资者教育信息站：在合规边界内，用自动化软件服务散户的真实信息需求——而非未持牌投顾或买卖信号。</p>
    <div class="meta-row">
      <span>报告日 {tables['meta']['as_of']}</span>
      <span>资金池 ¥1,000,000</span>
      <span>一人 · 周≤20小时</span>
      <span>可复现：python scripts/verify_all.py</span>
    </div>
  </header>

  <section id="exec">
    <h2>执行摘要</h2>
    <p class="section-lede">
      热词 <em>f stock</em> 指向散户对股票信息的检索需求。原「AI 情绪分析 + 个性化投资建议/买卖信号 SaaS」路径因投顾规制与一人约束不可执行，且旧数字无法复现。
      重选模式为<strong>{selected['name']}</strong>（加权分 {selected['weighted_score']:.2f}）。
    </p>
    <div class="metrics">
      <div class="metric">
        <div class="k">基准胜率 p</div>
        <div class="v">{fmt_pct(base_ret['win_prob'])}</div>
        <div class="s">现金成功（36月口径）</div>
      </div>
      <div class="metric">
        <div class="k">盈亏比 b</div>
        <div class="v">{fmt_x(base_ret['payoff_ratio_b'])}</div>
        <div class="s">(M_win−1)/损失倍数</div>
      </div>
      <div class="metric">
        <div class="k">风险调整年化</div>
        <div class="v">{fmt_pct(base_ret['ev']['r_risk_l0'])}</div>
        <div class="s">EV(L=0) 口径；保本上界 {fmt_pct(base_ret['ev']['r_risk_l1'])}</div>
      </div>
      <div class="metric">
        <div class="k">Kelly 建议配置</div>
        <div class="v">{fmt_cny(kelly['headline']['base_recommended_deploy_cny'])}</div>
        <div class="s">f*={fmt_pct(kelly['headline']['base_f_star'])} · 禁止全仓</div>
      </div>
    </div>
    <div class="danger">
      <strong>诚实结论：</strong>{kelly['headline']['statement']}
      {kelly_note}
    </div>
    <div class="callout">
      <strong>成功定义（可检验）：</strong>{base_ret['success_definition']}
      主目标不是讲故事式退出倍数，而是经营性现金回流与合规零重大处罚。
    </div>
  </section>

  <section id="compliance">
    <h2>合规边界与自我纠错</h2>
    <p class="section-lede">向善与合法优先：不能做的事明确说不能做。本报告不是投资建议，也不是法律意见。</p>
    <div class="warn">
      <strong>明确不做：</strong>个股买卖推荐、组合建议、交易信号、伪装成“教育”的投顾话术。
      美国《1940年投资顾问法》对以对价提供证券投资建议者施加注册义务；Lowe 案下的出版商排除要求非个性化、 bona fide、定期一般流通——个性化信号盘不在排除之列。
      因此变现以展示广告与「事实提醒」订阅为主，禁止保证收益话术。
    </div>
    <h3>对 need.txt 旧方案的批评</h3>
    <table>
      <thead><tr><th>指标</th><th>旧自报</th><th>按宣称参数复算</th><th>裁决</th></tr></thead>
      <tbody>
        <tr>
          <td>账面年化</td>
          <td>30%</td>
          <td>{fmt_pct(old['recalc_from_roi5']['r_book'])}（ROI5=1% → M=1.01）</td>
          <td class="neg">不一致</td>
        </tr>
        <tr>
          <td>期望倍数 EV</td>
          <td>1.5x</td>
          <td>{fmt_x(old['recalc_ev_band_using_claimed_p_and_m']['ev_l0'])}（亏光）~ {fmt_x(old['recalc_ev_band_using_claimed_p_and_m']['ev_l1'])}（保本）</td>
          <td class="neg">1.5x 落在区间外/不相容</td>
        </tr>
        <tr>
          <td>风险调整年化</td>
          <td>10%</td>
          <td>{fmt_pct(old['recalc_ev_band_using_claimed_p_and_m']['r_risk_l0'])} ~ {fmt_pct(old['recalc_ev_band_using_claimed_p_and_m']['r_risk_l1'])}</td>
          <td class="neg">不一致</td>
        </tr>
        <tr>
          <td>首年营收</td>
          <td>$1.5M（≈{fmt_cny(old_y1)}）</td>
          <td>一人/周20h/SEO冷启动下不可执行</td>
          <td class="neg">否决旧假设</td>
        </tr>
      </tbody>
    </table>
  </section>

  <section id="opportunity">
    <h2>机会重挖与评分</h2>
    <p class="section-lede">
      权重强调合规可做性与一人可执行性。策略生成器与个性化荐股因规制直接降权/否决。
      选定方案加权分 <strong>{selected['weighted_score']:.2f}</strong>。
    </p>
    <table>
      <thead>
        <tr>
          <th>机会</th><th>合规</th><th>一人</th><th>资本</th><th>自动化</th><th>需求</th><th>护城河</th><th>向善</th><th>加权</th>
        </tr>
      </thead>
      <tbody>{opp_rows_html}</tbody>
    </table>
    <h3>选定模式：无人信息站操作系统</h3>
    <div class="flow">
      <span>搜索需求</span><span class="arrow">→</span>
      <span>AI 内容/情绪数据流水线</span><span class="arrow">→</span>
      <span>公开信息站</span><span class="arrow">→</span>
      <span>广告</span><span class="arrow">/</span>
      <span>事实提醒</span><span class="arrow">→</span>
      <span>Stripe 自动计费</span><span class="arrow">→</span>
      <span>人·周20h闸门</span>
    </div>
    <div class="two-col">
      <div class="card-block">
        <h4>交付（可做）</h4>
        <ul>
          <li>公开源情绪/热度仪表盘与可复述方法</li>
          <li>新闻/公告溯源聚合（非建议）</li>
          <li>投资者教育内容与风险披露</li>
          <li>事实阈值提醒（“指标越过 X”，非买卖指令）</li>
        </ul>
      </div>
      <div class="card-block">
        <h4>变现（现实排序）</h4>
        <ul>
          <li>展示广告（英语金融 RPM 保守区间）</li>
          <li>低价事实提醒订阅（低转化）</li>
          <li>合规不确定的联盟收入（基准极低）</li>
        </ul>
      </div>
    </div>
  </section>

  <section id="market">
    <h2>市场与单位经济</h2>
    <p class="section-lede">
      股票软件/分析工具市场多源估计约数十亿至百亿美金量级（口径不一，报告用区间）。美国约 62% 成年人持有股票（Gallup 2025）；中介渠道零售投资者量级约数千万。
      SOM 不以「首年 5 万付费用户」幻想为准，而以 SEO 可达流量 × 极低转化建模。
      模型汇率：1 USD = {ue['fx']['usd_cny']} CNY（情景固定值，非预测）。
    </p>
    <h3>基准情景营收轨迹</h3>
    <div class="bars">{bars}</div>
    <div class="callout">
      RPM 假设（英语金融向）：保守 $2.5 / 基准 $5.0 / 乐观 $9.0 每千次浏览。
      付费 CAC 记为 0（有机 SEO）；内容与基础设施成本进入固定成本与 COGS。
    </div>
  </section>

  <section id="financials">
    <h2>五年财务（三情景）</h2>
    <p class="section-lede">
      相对旧稿“首年 $1.5M 营收”，本模型把一人精益约束写进数字。
      账面 ROI 路径描述<strong>成功情景下</strong>权益轨迹；经营 P&amp;L 为流量假设下的期望路径。
    </p>
    {fin_html}
  </section>

  <section id="returns">
    <h2>回报、胜率、盈亏比与风险调整年化</h2>
    <p class="section-lede">全部由 scripts/compute_returns.py 按统一口径计算，禁止口头圆数。</p>
    <div class="code">M_book = 1 + ROI5/100
r_book = M_book^(1/5) - 1
EV_L0 = p·M_win + (1-p)·0
EV_L1 = p·M_win + (1-p)·1
r_risk = EV^(1/5) - 1
b = (M_win - 1) / loss_of_stake</div>
    <table style="margin-top:20px">
      <thead>
        <tr>
          <th>情景</th><th>胜率 p</th><th>盈亏比 b</th><th>M_win</th>
          <th>账面年化</th><th>EV (L0/L1)</th><th>风险调整年化 (L0/L1)</th>
        </tr>
      </thead>
      <tbody>{ret_rows}</tbody>
    </table>
  </section>

  <section id="kelly">
    <h2>100 万资金池 · Kelly 最优比例</h2>
    <p class="section-lede">公式 f* = p − (1−p)/b；取半 Kelly，并硬约束 probe_cap=¥120,000。绝不 All-in。</p>
    <table>
      <thead>
        <tr><th>情景</th><th>p</th><th>b</th><th>f*</th><th>半Kelly</th><th>建议配置</th></tr>
      </thead>
      <tbody>{kelly_rows}</tbody>
    </table>
    <div class="danger" style="margin-top:18px">
      <strong>行动含义：</strong>若基准/保守情景 f*&lt;0，数学上不应把该机会当作正期望扩张仓位。
      允许的最大诚实动作是有上限的验证探针，用 Phase 关卡决定是否继续；未过关即停止加注。
    </div>
  </section>

  <section id="phases">
    <h2>阶段目标与可检验标准</h2>
    <p class="section-lede">{phases['stop_rule']}</p>
    {phase_html}
  </section>

  <section id="principles">
    <h2>风险、向善与工作原则对照</h2>
    <div class="two-col">
      <div class="card-block">
        <h4>主要矛盾</h4>
        <p class="small muted">情绪/信息需求真实，与投顾红线、一人产能冲突。解法是收缩到信息公开与教育，而不是硬做信号盘。</p>
      </div>
      <div class="card-block">
        <h4>价值优先</h4>
        <p class="small muted">先帮用户低成本理解公开情绪指标与风险披露，再谈广告分成；不靠制造焦虑或伪确定性收订阅。</p>
      </div>
      <div class="card-block">
        <h4>风险警觉</h4>
        <p class="small muted">对“高 ARPU 荐股订阅”“保证收益话术”保持拒绝。资金走正规渠道，财务闭环。</p>
      </div>
      <div class="card-block">
        <h4>自我革命</h4>
        <p class="small muted">旧稿数字已被脚本证伪并归档；此后以 verify_all.py 为质量闸门，小偏差早修。</p>
      </div>
    </div>
  </section>

  <section id="sources">
    <h2>数据来源与复现方法</h2>
    <p class="section-lede">
      假设入口：<code>scripts/assumptions.yaml</code>。一键复算：<code>python scripts/verify_all.py</code>。
      导出 PDF：<code>python scripts/export_pdf.py</code>。
    </p>
    <table>
      <thead><tr><th>字段</th><th>值</th><th>来源</th><th>备注</th></tr></thead>
      <tbody>{sources_html}</tbody>
    </table>
  </section>

  <footer class="footer">
    <p>版本 {tables['meta']['version']} · {tables['meta']['as_of']} · 本文件由 scripts/build_html.py 自计算结果生成。</p>
    <p>免责声明：本报告仅供商业机会研究与内部决策讨论，不构成证券投资建议或法律意见。最终决定权在人。</p>
  </footer>
</main>
</body>
</html>
"""
    return html


def main() -> Path:
    export_tables()
    tables = json.loads((COMPUTED_DIR / "tables.json").read_text(encoding="utf-8"))
    html = build(tables)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    out = REPORT_DIR / "index.html"
    out.write_text(html, encoding="utf-8")
    print("Wrote", out)
    return out


if __name__ == "__main__":
    main()
