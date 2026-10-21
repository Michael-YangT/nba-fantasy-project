from __future__ import annotations

from pathlib import Path
from flask import Flask, render_template

app = Flask(__name__, template_folder=str(Path(__file__).resolve().parent / "templates"))


SAMPLE_PLAYERS = [
    {"player_name": "Chet Holmgren", "position": "C", "final_score": 92.4, "injury_verdict": "ADD", "team": "OKC", "waiver_score": 88.1, "trade_score": 80.2},
    {"player_name": "Jalen Brunson", "position": "PG", "final_score": 82.1, "injury_verdict": "WATCH", "team": "NYK", "waiver_score": 74.5, "trade_score": 70.0},
    {"player_name": "Trey Murphy", "position": "SF", "final_score": 71.8, "injury_verdict": "WATCH", "team": "NOP", "waiver_score": 68.1, "trade_score": 64.4},
    {"player_name": "Domantas Sabonis", "position": "C", "final_score": 89.7, "injury_verdict": "ADD", "team": "SAC", "waiver_score": 80.5, "trade_score": 78.0},
    {"player_name": "Anthony Edwards", "position": "SG", "final_score": 77.6, "injury_verdict": "WATCH", "team": "MIN", "waiver_score": 72.9, "trade_score": 75.3},
]


@app.route("/")
def dashboard():
    return render_template("dashboard.html", players=SAMPLE_PLAYERS)


@app.route("/status")
def status():
    return {"status": "ok", "players": len(SAMPLE_PLAYERS), "app": "nba-fantasy-dashboard"}


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
