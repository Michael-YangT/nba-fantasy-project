from app.data.transform import derive_dd_td
from app.features.rolling import add_rolling_features
from app.features.efficiency import add_efficiency_features


def build_feature_dataset(df):
    df = derive_dd_td(df)
    df = add_rolling_features(df)
    df = add_efficiency_features(df)
    return df
