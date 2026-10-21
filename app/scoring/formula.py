from dataclasses import dataclass


@dataclass
class FantasyStats:
    minutes: float = 0.0
    fga: float = 0.0
    fta: float = 0.0
    ftm: float = 0.0
    three_pta: float = 0.0
    three_ptm: float = 0.0
    pts: float = 0.0
    oreb: float = 0.0
    reb: float = 0.0
    ast: float = 0.0
    st: float = 0.0
    blk: float = 0.0
    tov: float = 0.0
    dd: int = 0
    td: int = 0


def calc_player_score(stats: FantasyStats) -> float:
    score = (
        stats.minutes * (-0.25)
        + stats.fga * (-0.45)
        + stats.fta * (-0.75)
        + stats.ftm * 1.0
        + stats.three_pta * (-0.75)
        + stats.three_ptm * 3.0
        + stats.pts * 2.0
        + stats.oreb * 2.5
        + stats.reb * 1.0
        + stats.ast * 2.5
        + stats.st * 3.5
        + stats.blk * 3.5
        + stats.tov * (-2.0)
        + stats.dd * 10.0
        + stats.td * 20.0
    )
    return round(score, 2)
