import pandas as pd
from app.data.pipeline import run_etl
from app.strategy.constraints import DEFAULT_CONSTRAINTS
from app.strategy.lineup import optimize_lineup
from app.strategy.waiver import recommend_waivers
from app.strategy.trade import evaluate_trade_candidates
from app.injury.scorer import rank_injury_backfills
from app.notifications.template import build_daily_email_body
from app.notifications.smtp_client import send_email
from app.strategy.league_specific import rank_players
from app.strategy.weekly_context import matchup_score


def run_daily_job():
    run_etl()

    games = pd.read_parquet("processed/clean_player_games.parquet")
    roster = pd.read_parquet("processed/clean_roster.parquet")

    latest = games.sort_values("game_date").groupby("player_id", as_index=False).tail(1)

    rows = []
    for _, row in latest.iterrows():
        projected = {
            "minutes": row.get("minutes_7d_avg", 0.0),
            "fga": row.get("fga_7d_avg", 0.0),
            "fta": row.get("fta_7d_avg", 0.0),
            "ftm": row.get("ftm_7d_avg", 0.0),
            "three_pta": row.get("three_pta_7d_avg", 0.0),
            "three_ptm": row.get("three_ptm_7d_avg", 0.0),
            "pts": row.get("pts_7d_avg", 0.0),
            "oreb": row.get("oreb_7d_avg", 0.0),
            "reb": row.get("reb_7d_avg", 0.0),
            "ast": row.get("ast_7d_avg", 0.0),
            "st": row.get("st_7d_avg", 0.0),
            "blk": row.get("blk_7d_avg", 0.0),
            "tov": row.get("tov_7d_avg", 0.0),
        }

        score = (
            projected["minutes"] * (-0.25)
            + projected["fga"] * (-0.45)
            + projected["fta"] * (-0.75)
            + projected["ftm"] * 1.0
            + projected["three_pta"] * (-0.75)
            + projected["three_ptm"] * 3.0
            + projected["pts"] * 2.0
            + projected["oreb"] * 2.5
            + projected["reb"] * 1.0
            + projected["ast"] * 2.5
            + projected["st"] * 3.5
            + projected["blk"] * 3.5
            + projected["tov"] * (-2.0)
        )

        matchup_value = matchup_score(row.to_dict(), opponent_def_rating=110.0, pace=100.0, home=1)

        rows.append({
            "player_id": row["player_id"],
            "player_name": row.get("player_name", ""),
            "position": row.get("position", ""),
            "team": row.get("team", ""),
            "projected_score": round(score, 2),
            "risk_penalty": float(row.get("pts_volatility", 0.0)) * 3.0,
            "usage_gain": float(row.get("pts_7d_avg", 0.0) - row.get("pts_3d_avg", 0.0)),
            "role_stability": 1.0,
            "injury_risk": 0.0,
            "matchup": matchup_value,
            "minutes_gain": float(row.get("minutes_7d_avg", 0.0) - row.get("minutes_3d_avg", 0.0)),
            "usage_increase": float(row.get("pts_7d_avg", 0.0) - row.get("pts_3d_avg", 0.0)),
            "role_takeover": 0.6,
            "fantasy_fit": 4,
            "future_window": 7,
            "roster_need": 2,
            "injury_backfill": 4.0,
        })

    projected_df = pd.DataFrame(rows)
    merged = projected_df.merge(roster[["player_id", "player_name", "position", "team"]], on=["player_id", "player_name", "team"], how="left")
    players = merged.to_dict("records")

    lineup = optimize_lineup(players, DEFAULT_CONSTRAINTS)
    waivers = recommend_waivers(players)
    trade_candidates = evaluate_trade_candidates(players[:10])

    roster_state = {
        "need": {
            "PG": 1,
            "SG": 1,
            "SF": 1,
            "PF": 1,
            "C": 1,
            "UTIL": 1,
        }
    }

    league_recs = rank_players(players, roster_state)

    injury_candidates = [
        {
            "player_name": "Chet Holmgren",
            "minutes_gain": 8,
            "usage_increase": 7,
            "role_takeover": 0.8,
            "fantasy_fit": 4,
            "matchup": 4,
            "injury_risk": 3,
            "position": "C",
            "projected_score": 35,
            "roster_need": 5,
            "future_window": 7,
            "injury_backfill": 4.5,
        },
        {
            "player_name": "Trey Murphy",
            "minutes_gain": 4,
            "usage_increase": 3,
            "role_takeover": 0.4,
            "fantasy_fit": 4,
            "matchup": 3,
            "injury_risk": 3,
            "position": "SF",
            "projected_score": 24,
            "roster_need": 3,
            "future_window": 4,
            "injury_backfill": 3.0,
        },
        {
            "player_name": "Bam Adebayo",
            "minutes_gain": 2,
            "usage_increase": 1,
            "role_takeover": 0.2,
            "fantasy_fit": 3,
            "matchup": 2,
            "injury_risk": 4,
            "position": "C",
            "projected_score": 29,
            "roster_need": 2,
            "future_window": 2,
            "injury_backfill": 1.5,
        },
    ]

    ranked_injury = rank_injury_backfills(injury_candidates)
    classified = {
        "ADD": [p for p in ranked_injury if p.get("verdict") == "ADD"],
        "WATCH": [p for p in ranked_injury if p.get("verdict") == "WATCH"],
        "PASS": [p for p in ranked_injury if p.get("verdict") == "PASS"],
    }

    body = build_daily_email_body(lineup, waivers, classified["ADD"], league_recs)
    send_email("NBA Fantasy Daily Recommendation", body, "623254916@qq.com")

    print("lineup:", lineup)
    print("waivers:", waivers[:5])
    print("injury picks:", classified["ADD"])
    print("league_specific:", league_recs[:5])

    return {
        "lineup": lineup,
        "waivers": waivers[:10],
        "injury_picks": classified,
        "league_specific": league_recs[:10],
        "trades": trade_candidates[:10],
    }
