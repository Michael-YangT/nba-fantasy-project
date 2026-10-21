from typing import List, Dict


def normalize_position(position):
    if position is None:
        return ""
    pos = str(position).upper().strip()
    aliases = {
        "PG": "PG",
        "SG": "SG",
        "SF": "SF",
        "PF": "PF",
        "C": "C",
        "G": "G",
        "F": "F",
        "UTIL": "UTIL",
    }
    return aliases.get(pos, pos)


def adjusted_value(player):
    return player.get("projected_score", 0.0) - player.get("risk_penalty", 0.0) + player.get("upside_boost", 0.0)


def optimize_lineup(players: List[Dict], constraints: Dict) -> List[Dict]:
    normalized = []
    for p in players:
        p2 = dict(p)
        p2["position"] = normalize_position(p.get("position"))
        p2["slot_value"] = adjusted_value(p2)
        normalized.append(p2)

    ordered = sorted(normalized, key=lambda x: x["slot_value"], reverse=True)
    selected = []
    used = set()
    pos_counts = {k: 0 for k in constraints["position_slots"]}

    for p in ordered:
        pid = p.get("player_id")
        if pid in used:
            continue
        pos = p.get("position")
        if pos in constraints["position_slots"]:
            if pos_counts[pos] < constraints["position_slots"][pos]:
                selected.append(p)
                used.add(pid)
                pos_counts[pos] += 1

        if len(selected) >= constraints["max_players"]:
            break

    if len(selected) < constraints["max_players"]:
        for p in ordered:
            pid = p.get("player_id")
            if pid in used:
                continue
            selected.append(p)
            used.add(pid)
            if len(selected) >= constraints["max_players"]:
                break

    return selected
