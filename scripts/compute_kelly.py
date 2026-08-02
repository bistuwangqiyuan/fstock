"""
Kelly criterion for 1,000,000 CNY pool.

Binary approximation:
  f* = p - (1-p)/b
where b = net payoff ratio (net win / net loss of stake).

Also report half-Kelly, capped probe, and recommendation.
"""
from __future__ import annotations

from compute_returns import main as compute_returns
from lib_common import load_assumptions, write_json


def kelly_fraction(p: float, b: float) -> float:
    if b <= 0:
        return float("-inf")
    return p - (1.0 - p) / b


def main() -> dict:
    a = load_assumptions()
    returns = compute_returns()
    pool = float(a["capital"]["pool_cny"])
    probe_cap = float(a["capital"]["probe_cap_cny"])

    scenario_kelly = {}
    for sc, block in returns["scenarios"].items():
        p = block["win_prob"]
        b = block["payoff_ratio_b"]
        f = kelly_fraction(p, b)
        half = f / 2.0 if f > 0 else 0.0
        full_amt = max(0.0, f) * pool
        half_amt = half * pool
        # Recommended deploy: min(half-Kelly, probe_cap, scenario risk capital)
        recommended = min(half_amt if f > 0 else 0.0, probe_cap, block["risk_capital_cny"])
        if f <= 0:
            # Option-value probe still allowed but hard-capped and labeled non-Kelly
            recommended = min(probe_cap * 0.5, block["risk_capital_cny"])
            recommendation_note = (
                "Kelly f*≤0：数学上不应扩张风险本金；仅允许极小验证探针资本以获取信息期权。"
            )
        else:
            recommendation_note = (
                "采用半Kelly并受 probe_cap 与情景风险本金约束；禁止 All-in 全池。"
            )
        scenario_kelly[sc] = {
            "p": p,
            "b": b,
            "f_star": round(f, 6),
            "half_kelly": round(half, 6),
            "full_kelly_cny": round(full_amt, 2),
            "half_kelly_cny": round(half_amt, 2),
            "recommended_deploy_cny": round(recommended, 2),
            "recommended_fraction_of_pool": round(recommended / pool, 6),
            "note": recommendation_note,
        }

    base = scenario_kelly["base"]
    payload = {
        "version": a["version"],
        "as_of": a["as_of"],
        "pool_cny": pool,
        "probe_cap_cny": probe_cap,
        "formula": "f* = p - (1-p)/b ; half-Kelly = max(f*,0)/2",
        "scenarios": scenario_kelly,
        "headline": {
            "base_f_star": base["f_star"],
            "base_recommended_deploy_cny": base["recommended_deploy_cny"],
            "never_all_in": True,
            "statement": (
                f"对100万资金池，基准情景 Kelly f*={base['f_star']:.2%}；"
                f"建议配置约 ¥{base['recommended_deploy_cny']:,.0f}"
                f"（{base['recommended_fraction_of_pool']:.2%} 池），禁止全仓。"
            ),
        },
    }
    write_json("kelly.json", payload)
    return payload


if __name__ == "__main__":
    p = main()
    print(p["headline"]["statement"])
    for sc, b in p["scenarios"].items():
        print(sc, "f*", b["f_star"], "rec", b["recommended_deploy_cny"])
