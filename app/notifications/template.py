def build_daily_email_body(lineup, waivers, injury_candidates, league_recs=None):
    lines = ["NBA Fantasy Daily Recommendation", ""]
    lines.append("Recommended lineup:")
    for idx, p in enumerate(lineup[:8], start=1):
        lines.append(f"{idx}. {p['player_name']} ({p['position']}) - projected {p['projected_score']:.2f}")

    lines.append("")
    lines.append("Waiver targets:")
    for idx, p in enumerate(waivers[:5], start=1):
        lines.append(f"{idx}. {p['player_name']} ({p['position']}) - waiver {p['waiver_score']:.2f} | league {p.get('league_waiver_score', 0):.2f}")

    lines.append("")
    lines.append("Injury backfill picks:")
    for idx, p in enumerate(injury_candidates[:5], start=1):
        lines.append(f"{idx}. {p['player_name']} | verdict={p['verdict']} | score={p['score']}")

    if league_recs:
        lines.append("")
        lines.append("League-specific value list:")
        for idx, p in enumerate(league_recs[:5], start=1):
            lines.append(f"{idx}. {p['player_name']} | final_score={p['final_score']:.2f} | verdict={p['injury_verdict']} | fit={p['roster_fit']}")

    return "\n".join(lines)
