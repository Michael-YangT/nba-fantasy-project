import pandas as pd
from app.data.extract import load_csv
from app.data.transform import derive_dd_td
from app.features.rolling import add_rolling_features
from app.features.efficiency import add_efficiency_features
from app.data.load import save_parquet


def run_etl():
    games = load_csv("data/player_games.csv")
    roster = load_csv("data/player_roster.csv")
    injuries = load_csv("data/injuries.csv")
    lineups = load_csv("data/lineups.csv")
    team_context = load_csv("data/team_game_context.csv")

    for df in [games, roster, injuries, lineups, team_context]:
        if "game_date" in df.columns:
            df["game_date"] = pd.to_datetime(df["game_date"])
        if "player_id" in df.columns:
            df["player_id"] = df["player_id"].astype(str)
        if "reported_date" in df.columns:
            df["reported_date"] = pd.to_datetime(df["reported_date"])
        if "return_date" in df.columns:
            df["return_date"] = pd.to_datetime(df["return_date"])

    games = derive_dd_td(games)
    games = games.merge(team_context, on=["team", "opponent", "game_date"], how="left")
    games = add_rolling_features(games)
    games = add_efficiency_features(games)

    save_parquet(games, "processed/clean_player_games.parquet")
    save_parquet(roster, "processed/clean_roster.parquet")
    save_parquet(injuries, "processed/clean_injuries.parquet")
    save_parquet(lineups, "processed/clean_lineups.parquet")
    save_parquet(team_context, "processed/clean_team_context.parquet")

    print("ETL complete.")
