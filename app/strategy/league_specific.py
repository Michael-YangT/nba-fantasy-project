from typing import Dict, Any, List


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


def roster_fit_score(player: Dict[str, Any], roster_state: Dict[str, Any]) -> float:
    position = player.get("position", "")
    needs = roster_state.get("need", {})
    if position in needs:
        return float(needs[position]) * 2.0
    return 1.0


def weekly_h2h_value(player: Dict[str, Any], roster_state: Dict[str, Any], matchup: float) -> float:
    projected = player.get("projected_score", 0.0)
    role_takeover = player.get("role_takeover", 0.0)
    roster_need = roster_fit_score(player, roster_state)
    minutes_gain = player.get("minutes_gain", 0)

    return (
        projected * 0.5
        + role_takeover * 20
        + roster_need * 8
        + minutes_gain * 1.5
        + matchup * 3
    )


def league_waiver_score(player: Dict[str, Any]) -> float:
    projected_score = player.get("projected_score", 0.0)
    usage_increase = player.get("usage_increase", 0.0)
    minutes_gain = player.get("minutes_gain", 0.0)
    role_takeover = player.get("role_takeover", 0.0)
    roster_need = player.get("roster_need", 0)
    matchup = player.get("matchup", 3)
    injury_risk = player.get("injury_risk", 3)

    return (
        projected_score * 0.35
        + usage_increase * 2.2
        + minutes_gain * 1.8
        + role_takeover * 20
        + roster_need * 8
        + matchup * 3
        - injury_risk * 4
    )


def trade_value_score(player: Dict[str, Any], roster_state: Dict[str, Any]) -> float:
    base = player.get("projected_score", 0.0)
    role = player.get("role_takeover", 0.0)
    roster_need = roster_fit_score(player, roster_state)
    future_window = player.get("future_window", 0.0)

    return base * 0.5 + role * 15 + roster_need * 5 + future_window * 10


def league_specific_recommendation(player: Dict[str, Any], roster_state: Dict[str, Any], matchup: float = 3.0) -> Dict[str, Any]:
    injury_res = evaluate_injury_backfill(player)
    fit_score = roster_fit_score(player, roster_state)
    waiver_score = league_waiver_score(player)
    trade_score = trade_value_score(player, roster_state)
    weekly_value = weekly_h2h_value(player, roster_state, matchup)

    final_score = (
        waiver_score * 0.45
        + trade_score * 0.2
        + fit_score * 10
        + injury_res["score"] * 1.2
        + weekly_value * 0.35
    )

    return {
        "player_name": player.get("player_name"),
        "position": player.get("position"),
        "final_score": round(final_score, 2),
        "injury_verdict": injury_res["verdict"],
        "waiver_score": round(waiver_score, 2),
        "trade_score": round(trade_score, 2),
        "roster_fit": fit_score,
        "weekly_h2h_value": round(weekly_value, 2),
    }


def rank_players(players: List[Dict[str, Any]], roster_state: Dict[str, Any], matchup_map: Dict[str, float] = None) -> List[Dict[str, Any]]:
    if matchup_map is None:
        matchup_map = {}

    ranked = []
    for p in players:
        pos = p.get("position", "")
        matchup = matchup_map.get(pos, 3.0)
        rec = league_specific_recommendation(p, roster_state, matchup)
        ranked.append({**p, **rec})

    return sorted(ranked, key=lambda x: x["final_score"], reverse=True)
