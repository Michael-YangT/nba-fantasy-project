from app.scoring.formula import FantasyStats, calc_player_score


def score_from_dict(stats_dict):
    stats = FantasyStats(
        minutes=float(stats_dict.get("minutes", 0.0)),
        fga=float(stats_dict.get("fga", 0.0)),
        fta=float(stats_dict.get("fta", 0.0)),
        ftm=float(stats_dict.get("ftm", 0.0)),
        three_pta=float(stats_dict.get("three_pta", 0.0)),
        three_ptm=float(stats_dict.get("three_ptm", 0.0)),
        pts=float(stats_dict.get("pts", 0.0)),
        oreb=float(stats_dict.get("oreb", 0.0)),
        reb=float(stats_dict.get("reb", 0.0)),
        ast=float(stats_dict.get("ast", 0.0)),
        st=float(stats_dict.get("st", 0.0)),
        blk=float(stats_dict.get("blk", 0.0)),
        tov=float(stats_dict.get("tov", 0.0)),
        dd=int(stats_dict.get("dd", 0)),
        td=int(stats_dict.get("td", 0)),
    )
    return calc_player_score(stats)
