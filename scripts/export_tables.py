"""Run all compute modules and write aggregate tables.json for the HTML report."""
from __future__ import annotations

import json
from pathlib import Path

from compute_financials import main as compute_financials
from compute_kelly import main as compute_kelly
from compute_opportunity import main as compute_opportunity
from compute_returns import main as compute_returns
from compute_unit_economics import main as compute_unit_economics
from lib_common import COMPUTED_DIR, DATA_DIR, load_assumptions, write_json


def main() -> dict:
    a = load_assumptions()
    opp = compute_opportunity()
    ue = compute_unit_economics()
    fin = compute_financials()
    ret = compute_returns()
    kelly = compute_kelly()

    sources_path = DATA_DIR / "sources.json"
    sources = json.loads(sources_path.read_text(encoding="utf-8"))

    payload = {
        "meta": {
            "version": a["version"],
            "as_of": a["as_of"],
            "title": "F Stock · 全 AI 无人公司商业机会报告",
            "subtitle": "公开市场情绪与教育信息站 · 自有资金精益 · 可复现计算",
        },
        "opportunity": opp,
        "unit_economics": ue,
        "financials": fin,
        "returns": ret,
        "kelly": kelly,
        "sources": sources,
        "capital": a["capital"],
        "phases": {
            "phase0": {
                "name": "Phase 0 · 2周",
                "goals": [
                    "合规免责声明与禁词表上线（禁买卖建议/信号话术）",
                    "公开情绪指标方法说明页 + 教育落地页",
                    "合法公开数据源确认与自动发布跑通7天",
                ],
                "pass_criteria": [
                    "站点可访问且无个性化荐股/买卖信号",
                    "自动化流水线连续7日无人工救火",
                    "周维护工时记录 ≤20h",
                ],
            },
            "phase1": {
                "name": "Phase 1 · 至第3月",
                "goals": [
                    "扩展英语 SEO 主题簇（情绪/热度/教育）",
                    "SEO 内链与索引监测自动化",
                    "展示广告开通；评估提醒订阅试点",
                ],
                "pass_criteria": [
                    "有机点击与 RPM 可测且周报自动生成",
                    "广告收入 > 0 或明确卡点诊断",
                    "周维护仍 ≤20h",
                ],
            },
            "phase2": {
                "name": "Phase 2 · 至第12月",
                "goals": [
                    "事实提醒订阅试点（非投顾）",
                    "内容模板库与成本账本自动化",
                    "按止损规则复盘",
                ],
                "pass_criteria": [
                    "基准情景单位经济路径可解释",
                    "累计经营现金流趋势可核对",
                    "未达标则缩编或终止（执行半Kelly/探针上限）",
                ],
            },
            "stop_rule": (
                f"连续{a['capital']['stop_months_neg_contrib']}个月负贡献且SEO无斜率"
                "→ 下调风险本金或终止项目。"
            ),
        },
    }
    path = write_json("tables.json", payload)
    report_data = Path(__file__).resolve().parents[1] / "report" / "assets" / "tables.json"
    report_data.parent.mkdir(parents=True, exist_ok=True)
    report_data.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print("Wrote", path)
    print("Wrote", report_data)
    return payload


if __name__ == "__main__":
    main()
    print("computed files:", list(COMPUTED_DIR.glob("*.json")))
