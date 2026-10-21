import pandas as pd
from xgboost import XGBClassifier


class DTDModel:
    def __init__(self, target: str):
        self.target = target
        self.model = None

    def fit(self, X: pd.DataFrame, y: pd.Series):
        self.model = XGBClassifier(
            n_estimators=300,
            max_depth=4,
            learning_rate=0.05,
            random_state=42,
        )
        self.model.fit(X, y)

    def predict_proba(self, X: pd.DataFrame):
        if self.model is None:
            raise ValueError("Model not trained")
        return self.model.predict_proba(X)[:, 1]
