from typing import List, Dict
from app.injury.evaluator import evaluate_injury_backfill


def rank_injury_backfills(players: List[Dict]) -> List[Dict]:
    scored = []
    for p in players:
        result = evaluate_injury_backfill(p)
        merged = {**p, **result}
        scored.append(merged)
    return sorted(scored, key=lambda x: x["score"], reverse=True)
