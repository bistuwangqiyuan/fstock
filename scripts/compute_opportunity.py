"""Opportunity scoring matrix with explicit weights."""
from __future__ import annotations

from lib_common import load_assumptions, write_json


def weighted_score(scores: dict, weights: dict) -> float:
    total_w = sum(weights.values())
    s = sum(scores[k] * weights[k] for k in weights)
    return round(s / total_w, 4)


def main() -> dict:
    a = load_assumptions()
    weights = a["opportunity_weights"]
    rows = []
    for opp in a["opportunities"]:
        score = weighted_score(opp["scores"], weights)
        rows.append(
            {
                "id": opp["id"],
                "name": opp["name"],
                "selected": bool(opp.get("selected")),
                "veto_reason": opp.get("veto_reason"),
                "scores": opp["scores"],
                "weighted_score": score,
            }
        )
    rows.sort(key=lambda r: r["weighted_score"], reverse=True)
    selected = next(r for r in rows if r["selected"])
    # Guard: selected must be top among non-vetoed, or we flag inconsistency
    non_vetoed = [r for r in rows if not r.get("veto_reason")]
    top = non_vetoed[0]
    payload = {
        "version": a["version"],
        "as_of": a["as_of"],
        "weights": weights,
        "rows": rows,
        "selected_id": selected["id"],
        "selected_name": selected["name"],
        "top_non_vetoed_id": top["id"],
        "selection_consistent": selected["id"] == top["id"],
    }
    write_json("opportunity.json", payload)
    return payload


if __name__ == "__main__":
    out = main()
    print("Selected:", out["selected_name"], out["rows"][0]["weighted_score"])
    for r in out["rows"]:
        flag = "★" if r["selected"] else " "
        veto = f" [VETO: {r['veto_reason']}]" if r.get("veto_reason") else ""
        print(f"{flag} {r['weighted_score']:.2f}  {r['name']}{veto}")
