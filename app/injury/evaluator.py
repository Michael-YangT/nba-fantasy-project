from typing import Dict, Any


def evaluate_injury_backfill(player: Dict[str, Any]) -> Dict[str, Any]:
    minutes_gain = player.get("minutes_gain", 0)
    usage_increase = player.get("usage_increase", 0)
    role_takeover = player.get("role_takeover", 0.0)
    fantasy_fit = player.get("fantasy_fit", 3)
    matchup = player.get("matchup", 3)
    injury_risk = player.get("injury_risk", 3)

    if minutes_gain >= 8:
        minute_score = 5
    elif minutes_gain >= 5:
        minute_score = 4
    elif minutes_gain >= 3:
        minute_score = 3
    elif minutes_gain >= 1:
        minute_score = 2
    else:
        minute_score = 1

    if usage_increase >= 8:
        usage_score = 5
    elif usage_increase >= 5:
        usage_score = 4
    elif usage_increase >= 2:
        usage_score = 3
    elif usage_increase >= 1:
        usage_score = 2
    else:
        usage_score = 1

    if role_takeover >= 0.8:
        role_score = 5
    elif role_takeover >= 0.6:
        role_score = 4
    elif role_takeover >= 0.4:
        role_score = 3
    elif role_takeover >= 0.2:
        role_score = 2
    else:
        role_score = 1

    if fantasy_fit >= 5:
        fantasy_score = 5
    elif fantasy_fit >= 4:
        fantasy_score = 4
    elif fantasy_fit >= 3:
        fantasy_score = 3
    elif fantasy_fit >= 2:
        fantasy_score = 2
    else:
        fantasy_score = 1

    if matchup >= 5:
        matchup_score = 5
    elif matchup >= 4:
        matchup_score = 4
    elif matchup >= 3:
        matchup_score = 3
    elif matchup >= 2:
        matchup_score = 2
    else:
        matchup_score = 1

    if injury_risk <= 2:
        risk_score = 5
    elif injury_risk <= 3:
        risk_score = 4
    elif injury_risk <= 4:
        risk_score = 3
    else:
        risk_score = 2

    total = (
        minute_score * 1.2
        + usage_score * 1.3
        + role_score * 1.3
        + fantasy_score * 1.1
        + matchup_score * 0.9
        + risk_score * 0.8
    )

    verdict = "ADD" if total >= 22 else "WATCH" if total >= 18 else "PASS"

    return {
        "player_name": player.get("player_name"),
        "minutes_gain": minutes_gain,
        "usage_increase": usage_increase,
        "role_takeover": role_takeover,
        "fantasy_fit": fantasy_fit,
        "matchup": matchup,
        "injury_risk": injury_risk,
        "score": round(total, 2),
        "verdict": verdict,
    }
