# NBA Fantasy Recommendation Engine

This project builds a fantasy NBA recommendation system for a 14-team H2H points league with deep roster structure, 4 IL spots, 2 UTIL slots, and a trade-friendly roster environment.

Features:
- ETL pipeline for player, lineup, injury, and team context data
- rolling stat and efficiency features
- XGBoost-based stat projection
- fantasy scoring formula
- roster-aware lineup optimizer
- waiver and trade recommendations
- injury backfill scoring for deep leagues
- quick email notifications for daily recommendations

League profile supported:
- 14 teams
- H2H points format
- 16 roster slots
- 4 IL slots
- 2 UTIL slots
- deep roster with role flexibility
- no waiver friction / free-agent adds are relevant
- trade-friendly environment

Fantasy scoring formula used:
- MIN * (-0.25)
- FGA * (-0.45)
- FTA * (-0.75)
- FTM * 1.0
- 3PTA * (-0.75)
- 3PTM * 3.0
- PTS * 2.0
- OREB * 2.5
- REB * 1.0
- AST * 2.5
- STL * 3.5
- BLK * 3.5
- TOV * (-2.0)
- DD * 10.0
- TD * 20.0

Quick start:
1. Copy .env.example to .env and fill in your QQ SMTP details.
2. Put the CSV files under data/.
3. Install dependencies:
   pip install -r requirements.txt
4. Run the project:
   python run.py

The script will:
- clean and transform data
- build rolling and efficiency features
- generate projected values
- optimize lineup against league constraints
- identify waiver and trade opportunities
- flag injury replacement candidates
- send a daily email recommendation
