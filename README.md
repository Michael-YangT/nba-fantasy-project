# NBA Fantasy Recommendation Engine

This project builds a fantasy NBA recommendation system optimized for a deep 14-team H2H points league.

It includes:
- data ingestion and ETL
- rolling features and efficiency features
- XGBoost-based projection scaffolding
- simulation and backtest utilities
- lineup, waiver, injury, and trade recommendation modules
- weekly matchup and roster-fit logic
- dashboard web UI
- scheduler for daily automated recommendations
- SMTP email alerts

League profile supported:
- 14 teams
- H2H points
- 16 roster slots
- 4 IL slots
- 2 UTIL slots
- deep roster value / injury replacement importance
- trade friendly environment
- no waiver friction

Quick start:
1. Install dependencies:
   pip install -r requirements.txt
2. Copy example env file:
   cp .env.example .env
3. Configure SMTP credentials in `.env`.
4. Launch the dashboard:
   python app/dashboard/app.py
5. Or run the project job:
   python run.py
6. Or run scheduler:
   python app/jobs/scheduler.py

Key modules:
- app/strategy/league_specific.py : league-aware add / waiver / trade recommendations
- app/strategy/weekly_context.py : matchup scoring by pace and opponent rating
- app/strategy/seasonal.py : positional value, upside, schedule strength, trade value
- app/models/backtest.py : backtest utilities and strategy simulation
- app/dashboard/app.py : Flask dashboard
- app/jobs/daily_recommendation.py : main recommendation workflow
- app/jobs/scheduler.py : daily cron scheduling

Production notes:
- For real data, replace the sample CSV files in `data/`.
- Use your own SMTP credentials in `.env`.
- You can extend the model training pipeline in `app/models/train.py` and backtesting in `app/models/backtest.py`.
