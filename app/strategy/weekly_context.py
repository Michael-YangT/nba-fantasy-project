from typing import Dict, Any


def matchup_score(player: Dict[str, Any], opponent_def_rating: float = 110.0, pace: float = 100.0, home: int = 1) -> float:
    score = 0.0

    if opponent_def_rating >= 115:
        score -= 1.0
    elif opponent_def_rating <= 108:
        score += 2.0

    if pace >= 102:
        score += 1.0
    elif pace <= 98:
        score -= 0.5

    if home == 1:
        score += 1.0

    pos = player.get("position", "")
    if pos in {"PG", "SG", "SF"}:
        score += 0.5
    if pos in {"PF", "C"}:
        score += 0.3

    return round(score, 2)
