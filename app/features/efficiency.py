import pandas as pd


def add_efficiency_features(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()

    if "ftm" in out.columns and "fga" in out.columns:
        out["fg_pct"] = out["ftm"] / out["fga"].replace(0, 1)
    if "three_ptm" in out.columns and "three_pta" in out.columns:
        out["three_pt_pct"] = out["three_ptm"] / out["three_pta"].replace(0, 1)
    if "ftm" in out.columns and "fta" in out.columns:
        out["ft_pct"] = out["ftm"] / out["fta"].replace(0, 1)
    if "ast" in out.columns and "tov" in out.columns:
        out["ast_tov_ratio"] = out["ast"] / out["tov"].replace(0, 1)
    if "oreb" in out.columns and "reb" in out.columns:
        out["oreb_reb_ratio"] = out["oreb"] / out["reb"].replace(0, 1)

    return out
