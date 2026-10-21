from typing import List, Dict


def filter_injury_candidates(players: List[Dict]) -> Dict[str, List[Dict]]:
    add_list = []
    watch_list = []
    pass_list = []

    for p in players:
        verdict = p.get("verdict", "PASS")
        if verdict == "ADD":
            add_list.append(p)
        elif verdict == "WATCH":
            watch_list.append(p)
        else:
            pass_list.append(p)

    return {
        "ADD": add_list,
        "WATCH": watch_list,
        "PASS": pass_list,
    }
