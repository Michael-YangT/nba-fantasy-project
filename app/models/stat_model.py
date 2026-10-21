import pandas as pd
from xgboost import XGBRegressor


class StatModel:
    def __init__(self, target: str):
        self.target = target
        self.model = None

    def fit(self, X: pd.DataFrame, y: pd.Series):
        self.model = XGBRegressor(
            n_estimators=500,
            max_depth=6,
            learning_rate=0.05,
            subsample=0.9,
            colsample_bytree=0.8,
            random_state=42,
        )
        self.model.fit(X, y)

    def predict(self, X: pd.DataFrame):
        if self.model is None:
            raise ValueError("Model not trained")
        return self.model.predict(X)
