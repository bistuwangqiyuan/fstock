"""
Return metrics with forced reproducible formulas:

  M_book = 1 + ROI5/100
  r_book = M_book ** (1/5) - 1
  EV_L0 = p * M_win + (1-p) * 0
  EV_L1 = p * M_win + (1-p) * 1
  r_risk = EV ** (1/5) - 1
  payoff_ratio b = (M_win - 1) / loss_of_stake   # net gain / net loss of stake
"""
from __future__ import annotations

from lib_common import load_assumptions, write_json


def book_metrics(roi5_pct: float, horizon: int = 5) -> dict:
    m = 1.0 + roi5_pct / 100.0
    if m <= 0:
        r = None
    else:
        r = m ** (1.0 / horizon) - 1.0
    return {"m_book": round(m, 6), "r_book": None if r is None else round(r, 6), "roi5_pct": roi5_pct}


def ev_metrics(p: float, m_win: float, horizon: int = 5) -> dict:
    ev0 = p * m_win + (1.0 - p) * 0.0
    ev1 = p * m_win + (1.0 - p) * 1.0
    r0 = ev0 ** (1.0 / horizon) - 1.0 if ev0 > 0 else -1.0
    r1 = ev1 ** (1.0 / horizon) - 1.0 if ev1 > 0 else -1.0
    return {
        "p": p,
        "m_win": m_win,
        "ev_l0": round(ev0, 6),
        "ev_l1": round(ev1, 6),
        "r_risk_l0": round(r0, 6),
        "r_risk_l1": round(r1, 6),
    }


def payoff_ratio(m_win: float, loss_of_stake: float) -> float:
    # Net gain multiple of stake if win: (M_win - 1); net loss multiple if lose: loss_of_stake
    return (m_win - 1.0) / loss_of_stake


def main() -> dict:
    a = load_assumptions()
    ret = a["returns"]
    horizon = ret["horizon_years"]
    loss = ret["loss_of_stake"]

    scenarios = {}
    for sc in ["conservative", "base", "optimistic"]:
        roi_path = ret["book_roi_pct"][sc]
        book = book_metrics(roi_path[-1], horizon)
        # Map scenario to win prob band
        p_map = {"conservative": "low", "base": "mid", "optimistic": "high"}
        p = ret["win_prob"][p_map[sc]]
        m_win = ret["m_win"][sc]
        b = payoff_ratio(m_win, loss)
        ev = ev_metrics(p, m_win, horizon)
        scenarios[sc] = {
            "risk_capital_cny": ret["risk_capital_cny"][sc],
            "book_roi_path_pct": roi_path,
            "book": book,
            "win_prob": p,
            "m_win": m_win,
            "payoff_ratio_b": round(b, 6),
            "ev": ev,
            "success_definition": (
                "36个月内累计经营现金流≥风险本金，且无重大合规处罚；"
                "退出事件为次要情景，不计入主胜率除非单独标注。"
            ),
        }

    # Mid-case explicit band using mid p with base m_win, plus p band sensitivity
    p_low, p_mid, p_high = (
        ret["win_prob"]["low"],
        ret["win_prob"]["mid"],
        ret["win_prob"]["high"],
    )
    m_base = ret["m_win"]["base"]
    sensitivity = {
        "p_low": ev_metrics(p_low, m_base, horizon),
        "p_mid": ev_metrics(p_mid, m_base, horizon),
        "p_high": ev_metrics(p_high, m_base, horizon),
        "payoff_ratio_at_base_m": round(payoff_ratio(m_base, loss), 6),
    }

    # Reproduce old need.txt contradiction for appendix
    old = a["old_need_claims"]
    old_recalc = {
        "claimed": old,
        "recalc_from_roi5": book_metrics(old["claimed_roi5_pct"], horizon),
        "recalc_ev_band_using_claimed_p_and_m": {
            "p": old["claimed_win_rate_mid"],
            "m": old["claimed_m_from_roi5"],
            **ev_metrics(old["claimed_win_rate_mid"], old["claimed_m_from_roi5"], horizon),
        },
    }

    payload = {
        "version": a["version"],
        "as_of": a["as_of"],
        "formulas": {
            "m_book": "1 + ROI5/100",
            "r_book": "M_book ** (1/5) - 1",
            "ev_l0": "p * M_win + (1-p) * 0",
            "ev_l1": "p * M_win + (1-p) * 1",
            "r_risk": "EV ** (1/5) - 1",
            "payoff_ratio_b": "(M_win - 1) / loss_of_stake",
        },
        "scenarios": scenarios,
        "sensitivity_base_m": sensitivity,
        "old_need_audit": old_recalc,
    }
    write_json("returns.json", payload)
    return payload


if __name__ == "__main__":
    p = main()
    b = p["scenarios"]["base"]
    print("base r_book", b["book"]["r_book"], "b", b["payoff_ratio_b"])
    print("base EV", b["ev"])
    print("old audit", p["old_need_audit"]["recalc_from_roi5"])
