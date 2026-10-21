import pandas as pd


def derive_dd_td(df: pd.DataFrame) -> pd.DataFrame:
    if "dd" not in df.columns:
        df["dd"] = (
            (df["reb"] >= 10)
            | (df["ast"] >= 10)
            | (df["pts"] >= 10)
            | (df["st"] >= 10)
            | (df["blk"] >= 10)
        ).astype(int)

    if "td" not in df.columns:
        df["td"] = (
            (df["reb"] >= 10)
            & (df["ast"] >= 10)
            & (df["pts"] >= 10)
        ).astype(int)

    return df
