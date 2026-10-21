import pandas as pd
from app.models.stat_model import StatModel
from app.models.dd_td_model import DTDModel


def train_models(df: pd.DataFrame):
    feature_candidates = [
        "minutes_7d_avg", "pts_7d_avg", "reb_7d_avg", "ast_7d_avg", "st_7d_avg",
        "blk_7d_avg", "three_ptm_7d_avg", "tov_7d_avg",
        "fg_pct", "three_pt_pct", "ft_pct", "ast_tov_ratio", "oreb_reb_ratio",
        "pts_volatility", "opp_def_rating", "pace", "rest_days", "back_to_back", "home"
    ]
    feature_cols = [c for c in feature_candidates if c in df.columns]

    models = {}
    for target in ["pts", "reb", "ast", "st", "blk", "three_ptm", "tov", "minutes"]:
        if target in df.columns:
            model = StatModel(target)
            model.fit(df[feature_cols], df[target])
            models[target] = model

    dd_model = DTDModel("dd")
    dd_model.fit(df[feature_cols], df["dd"])

    td_model = DTDModel("td")
    td_model.fit(df[feature_cols], df["td"])

    return models, dd_model, td_model, feature_cols
