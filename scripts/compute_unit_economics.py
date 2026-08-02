"""Unit economics: ads + alerts + affiliate per scenario/year (USD alerts)."""
from __future__ import annotations

from lib_common import load_assumptions, write_json

YEARS = ["y1", "y2", "y3", "y4", "y5"]
SCENARIOS = ["conservative", "base", "optimistic"]


def annual_ads_cny(pageviews_month: float, rpm_usd: float, usd_cny: float) -> float:
    # monthly pageviews * 12 / 1000 * RPM_USD * FX
    return pageviews_month * 12.0 / 1000.0 * rpm_usd * usd_cny


def annual_alert_cny(
    pageviews_month: float,
    conversion: float,
    arpu_usd_month: float,
    usd_cny: float,
) -> float:
    # Approximate MAU ≈ monthly pageviews * 0.55 (multi-page sessions)
    mau = pageviews_month * 0.55
    paying = mau * conversion
    return paying * arpu_usd_month * 12.0 * usd_cny


def main() -> dict:
    a = load_assumptions()
    fx = a["fx"]
    ue = a["unit_economics"]
    out_scenarios = {}

    for sc in SCENARIOS:
        years = []
        for y in YEARS:
            pv = ue["monthly_pageviews"][y][sc]
            ads = annual_ads_cny(pv, ue["rpm_usd"][sc], fx["usd_cny"])
            alerts = annual_alert_cny(
                pv,
                ue["alert_pay_conversion"][sc],
                ue["alert_arpu_usd_month"][sc],
                fx["usd_cny"],
            )
            affiliate = float(ue["affiliate_cny_year"][sc][y])
            revenue = ads + alerts + affiliate
            cogs = revenue * ue["cogs_ratio"][sc]
            fixed = float(ue["fixed_cost_cny_year"][sc][y])
            ebitda = revenue - cogs - fixed
            years.append(
                {
                    "year": y,
                    "monthly_pageviews": pv,
                    "ads_cny": round(ads, 2),
                    "alerts_cny": round(alerts, 2),
                    "affiliate_cny": round(affiliate, 2),
                    "revenue_cny": round(revenue, 2),
                    "cogs_cny": round(cogs, 2),
                    "fixed_cny": round(fixed, 2),
                    "ebitda_cny": round(ebitda, 2),
                    "rpm_usd": ue["rpm_usd"][sc],
                    "paid_cac_cny": ue["paid_cac_cny"][sc],
                }
            )
        cum = 0.0
        payback_year = None
        for row in years:
            cum += row["ebitda_cny"]
            row["cumulative_ebitda_cny"] = round(cum, 2)
            if payback_year is None and cum >= a["returns"]["risk_capital_cny"][sc]:
                payback_year = row["year"]
        out_scenarios[sc] = {
            "years": years,
            "payback_vs_risk_capital_year": payback_year,
            "y5_revenue_cny": years[-1]["revenue_cny"],
            "y5_ebitda_cny": years[-1]["ebitda_cny"],
            "y5_cum_ebitda_cny": years[-1]["cumulative_ebitda_cny"],
        }

    payload = {
        "version": a["version"],
        "as_of": a["as_of"],
        "fx": fx,
        "scenarios": out_scenarios,
        "notes": [
            ue.get("note_cac"),
            "Alert MAU approximated as 55% of monthly pageviews.",
            "Affiliate path is compliance-uncertain; kept small in base.",
        ],
    }
    write_json("unit_economics.json", payload)
    return payload


if __name__ == "__main__":
    p = main()
    for sc, block in p["scenarios"].items():
        print(
            sc,
            "Y5 rev",
            block["y5_revenue_cny"],
            "Y5 ebitda",
            block["y5_ebitda_cny"],
            "payback",
            block["payback_vs_risk_capital_year"],
        )
