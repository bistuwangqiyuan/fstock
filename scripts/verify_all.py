"""End-to-end verification: recompute, assert self-consistency, audit old need.txt claims."""
from __future__ import annotations

import math
import sys

from compute_kelly import kelly_fraction
from compute_returns import book_metrics, ev_metrics, payoff_ratio
from export_tables import main as export_tables
from lib_common import load_assumptions


def approx_eq(a: float, b: float, tol: float = 1e-9) -> bool:
    return abs(a - b) <= tol


def main() -> int:
    a = load_assumptions()
    tables = export_tables()
    errors: list[str] = []

    # 1) Selection consistency
    if not tables["opportunity"]["selection_consistent"]:
        errors.append("Selected opportunity is not top among non-vetoed options.")

    # 2) Formula self-check on base scenario
    base_ret = tables["returns"]["scenarios"]["base"]
    roi5 = base_ret["book_roi_path_pct"][-1]
    bm = book_metrics(roi5, a["returns"]["horizon_years"])
    if not approx_eq(bm["m_book"], base_ret["book"]["m_book"]):
        errors.append("Book M mismatch.")
    if not approx_eq(bm["r_book"], base_ret["book"]["r_book"]):
        errors.append("Book annualized mismatch.")

    p = base_ret["win_prob"]
    m_win = base_ret["m_win"]
    ev = ev_metrics(p, m_win, a["returns"]["horizon_years"])
    for k in ("ev_l0", "ev_l1", "r_risk_l0", "r_risk_l1"):
        if not approx_eq(ev[k], base_ret["ev"][k]):
            errors.append(f"EV field mismatch: {k}")

    b = payoff_ratio(m_win, a["returns"]["loss_of_stake"])
    if not approx_eq(b, base_ret["payoff_ratio_b"]):
        errors.append("Payoff ratio mismatch.")

    # 3) Kelly identity
    f = kelly_fraction(p, b)
    if not approx_eq(f, tables["kelly"]["scenarios"]["base"]["f_star"], tol=1e-6):
        errors.append("Kelly f* mismatch.")

    # 4) Never recommend all-in
    for sc, block in tables["kelly"]["scenarios"].items():
        if block["recommended_deploy_cny"] > a["capital"]["pool_cny"] * 0.5 + 1e-6:
            errors.append(f"{sc}: recommended deploy exceeds 50% pool safety bound.")
        if block["recommended_deploy_cny"] > a["capital"]["probe_cap_cny"] + 1e-6:
            errors.append(f"{sc}: recommended deploy exceeds probe_cap.")

    # 5) Old need contradiction must be visible and numerically confirmed
    old = tables["returns"]["old_need_audit"]
    recalc_r = old["recalc_from_roi5"]["r_book"]
    claimed_r = a["old_need_claims"]["claimed_book_annualized"]
    if abs(recalc_r - claimed_r) < 0.05:
        errors.append("Expected old claimed book annualized to diverge from ROI5 recalc.")
    # need.txt ROI5=1% → M=1.01 → r = 1.01^(1/5)-1
    expect = (1 + 0.01) ** 0.2 - 1
    if not math.isclose(recalc_r, expect, rel_tol=0, abs_tol=1e-4):
        errors.append(f"Old ROI5 recalc expected ~{expect}, got {recalc_r}")

    ev_band = old["recalc_ev_band_using_claimed_p_and_m"]
    p_old = a["old_need_claims"]["claimed_win_rate_mid"]
    m_old = a["old_need_claims"]["claimed_m_from_roi5"]
    expect_l0 = p_old * m_old
    expect_l1 = p_old * m_old + (1.0 - p_old) * 1.0
    if not math.isclose(ev_band["ev_l0"], expect_l0, abs_tol=1e-6):
        errors.append(f"Old EV L0 should be {expect_l0}, got {ev_band['ev_l0']}")
    if not math.isclose(ev_band["ev_l1"], expect_l1, abs_tol=1e-6):
        errors.append(f"Old EV L1 should be {expect_l1}, got {ev_band['ev_l1']}")
    claimed_ev = a["old_need_claims"]["claimed_ev_moic"]
    if not (ev_band["ev_l0"] < claimed_ev):
        errors.append("Claimed EV should sit above L0 band under old inconsistent params.")

    # 6) Financial realism vs old fantasy
    base_y1 = tables["financials"]["scenarios"]["base"]["rows"][0]["revenue_cny"]
    if base_y1 >= 1_000_000:
        errors.append("Base Y1 revenue still unrealistically high for solo lean model.")
    old_y1_cny = tables["financials"]["contrast_old_need"]["old_y1_to_y5_revenue_cny"][0]
    if base_y1 >= old_y1_cny * 0.1:
        # Old Y1 was $1.5M ≈ ¥10.8M; new base must be << 10% of that fantasy
        errors.append("Base Y1 not sufficiently below old need fantasy revenue.")

    # 7) Vetoed opportunities must have low compliance
    for row in tables["opportunity"]["rows"]:
        if row.get("veto_reason") and row["scores"]["compliance"] >= 5:
            errors.append(f"Vetoed opp {row['id']} has unexpectedly high compliance score.")

    if errors:
        print("VERIFY FAIL")
        for e in errors:
            print(" -", e)
        return 1

    print("VERIFY PASS")
    print("Selected:", tables["opportunity"]["selected_name"])
    print("Base book annualized:", f"{base_ret['book']['r_book']*100:.2f}%")
    print(
        "Base EV L0/L1:",
        base_ret["ev"]["ev_l0"],
        "/",
        base_ret["ev"]["ev_l1"],
    )
    print(
        "Base risk-adj ann L0/L1:",
        f"{base_ret['ev']['r_risk_l0']*100:.2f}%",
        "/",
        f"{base_ret['ev']['r_risk_l1']*100:.2f}%",
    )
    print("Base Kelly f*:", tables["kelly"]["scenarios"]["base"]["f_star"])
    print("Recommended deploy CNY:", tables["kelly"]["headline"]["base_recommended_deploy_cny"])
    print(
        "Old need book ann claimed 30% vs recalc",
        f"{recalc_r*100:.2f}%",
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
