"""Five-year P&L summary from unit economics (three scenarios)."""
from __future__ import annotations

from compute_unit_economics import main as compute_ue
from lib_common import load_assumptions, write_json


def main() -> dict:
    a = load_assumptions()
    ue = compute_ue()
    usd_cny = float(a["fx"]["usd_cny"])
    old_usd = a["old_need_claims"]["claimed_y1_revenue_usd"]
    # Old need Y1–Y5 USD revenues from need.txt
    old_usd_path = [1_500_000, 5_000_000, 12_000_000, 20_000_000, 30_000_000]
    scenarios = {}
    for sc, block in ue["scenarios"].items():
        rows = []
        for i, y in enumerate(block["years"]):
            rows.append(
                {
                    "year_index": i + 1,
                    "year_key": y["year"],
                    "revenue_cny": y["revenue_cny"],
                    "ebitda_cny": y["ebitda_cny"],
                    "cumulative_ebitda_cny": y["cumulative_ebitda_cny"],
                    "book_roi_pct": a["returns"]["book_roi_pct"][sc][i],
                }
            )
        scenarios[sc] = {
            "risk_capital_cny": a["returns"]["risk_capital_cny"][sc],
            "rows": rows,
            "payback_vs_risk_capital_year": block["payback_vs_risk_capital_year"],
        }

    payload = {
        "version": a["version"],
        "as_of": a["as_of"],
        "pool_cny": a["capital"]["pool_cny"],
        "scenarios": scenarios,
        "contrast_old_need": {
            "old_y1_to_y5_revenue_usd": old_usd_path,
            "old_y1_to_y5_revenue_cny": [round(x * usd_cny, 2) for x in old_usd_path],
            "old_y1_revenue_usd": old_usd,
            "note": (
                "Old need.txt figures are not reproducible under solo/20h/compliance "
                "constraints; replaced by SEO+Ads lean model."
            ),
        },
    }
    write_json("financials.json", payload)
    return payload


if __name__ == "__main__":
    p = main()
    for sc, block in p["scenarios"].items():
        print(sc, [(r["revenue_cny"], r["ebitda_cny"]) for r in block["rows"]])
