from typing import List, Dict


def recommend_waivers(players: List[Dict]) -> List[Dict]:
    ranked = []
    for p in players:
        usage_gain = p.get("usage_gain", 0.0)
        role_stability = p.get("role_stability", 0.0)
        injury_risk = p.get("injury_risk", 0.0)
        projected = p.get("projected_score", 0.0)

        waiver_score = (
            projected
            + usage_gain * 2.0
            + role_stability * 1.5
            - injury_risk * 3.0
        )

        p2 = dict(p)
        p2["waiver_score"] = waiver_score
        p2["league_waiver_score"] = round(waiver_score, 2)
        ranked.append(p2)

    return sorted(ranked, key=lambda x: x["league_waiver_score"], reverse=True)
