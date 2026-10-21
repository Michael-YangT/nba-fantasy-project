from typing import List, Dict


def analyze_trade(player_a: Dict, player_b: Dict) -> Dict:
    delta = player_a.get("projected_score", 0.0) - player_b.get("projected_score", 0.0)
    return {
        "player_a": player_a.get("player_name"),
        "player_b": player_b.get("player_name"),
        "projected_delta": round(delta, 2),
        "verdict": "A is better" if delta > 0 else "B is better",
    }


def evaluate_trade_candidates(players: List[Dict]) -> List[Dict]:
    results = []
    n = min(len(players), 10)
    for i in range(n):
        for j in range(i + 1, n):
            results.append(analyze_trade(players[i], players[j]))
    return results
