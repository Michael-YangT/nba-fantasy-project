from __future__ import annotations

from typing import Any, Dict, List
import math
import pandas as pd


def score_pred_vs_actual(actual: pd.Series, predicted: pd.Series) -> Dict[str, float]:
    errors = (actual - predicted).abs()
    mae = float(errors.mean())
    rmse = float(math.sqrt(( (actual - predicted) ** 2 ).mean()))
    mape = float((errors / actual.replace(0, 1)).mean())
    return {
        "mae": round(mae, 4),
        "rmse": round(rmse, 4),
        "mape": round(mape, 4),
    }


def run_backtest(df: pd.DataFrame, target: str = "pts") -> Dict[str, Any]:
    if df.empty:
        return {"message": "No data for backtest", "mae": 0.0, "rmse": 0.0, "mape": 0.0}

    required = {"player_id", "game_date", target}
    if not required.issubset(df.columns):
        raise ValueError(f"Backtest requires columns: {required}")

    df = df.sort_values(["player_id", "game_date"]).copy()
    df["lag_pred"] = df.groupby("player_id")[target].shift(1).fillna(df[target].mean())
    metrics = score_pred_vs_actual(df[target].fillna(0), df["lag_pred"].fillna(0))

    return {
        "target": target,
        "games": int(len(df)),
        "players": int(df["player_id"].nunique()),
        "metrics": metrics,
        "summary": {
            "avg_actual": round(float(df[target].mean()), 2),
            "avg_pred": round(float(df["lag_pred"].mean()), 2),
        },
    }


def simulate_strategy_performance(df: pd.DataFrame) -> Dict[str, Any]:
    if df.empty:
        return {"strategy": "none", "score": 0.0}

    df = df.copy()
    df["strategy_signal"] = df.get("usage_increase", 0) + df.get("minutes_gain", 0) + df.get("role_takeover", 0) * 10
    df["strategy_score"] = df["strategy_signal"] * df.get("projected_score", 0)

    return {
        "strategy": "usage_role_signal",
        "mean_signal": round(float(df["strategy_signal"].mean()), 2),
        "mean_strategy_score": round(float(df["strategy_score"].mean()), 2),
    }
