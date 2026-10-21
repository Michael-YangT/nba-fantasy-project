import pandas as pd


def add_rolling_features(df: pd.DataFrame) -> pd.DataFrame:
    out = df.sort_values(["player_id", "game_date"]).copy()

    stats = [
        "minutes", "pts", "reb", "ast", "st", "blk", "tov",
        "fga", "fta", "ftm", "three_pta", "three_ptm", "oreb", "dd", "td"
    ]

    for window in [3, 7, 14, 28]:
        for col in stats:
            if col in out.columns:
                out[f"{col}_{window}d_avg"] = (
                    out.groupby("player_id")[col]
                    .transform(lambda s: s.shift(1).rolling(window, min_periods=1).mean())
                )

    if "pts" in out.columns:
        out["pts_volatility"] = (
            out.groupby("player_id")["pts"]
            .transform(lambda s: s.pct_change().fillna(0).abs().rolling(5, min_periods=1).mean())
        )

    return out
