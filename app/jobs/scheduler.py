from __future__ import annotations

from typing import Dict, Any
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from app.jobs.daily_recommendation import run_daily_job


def start_scheduler():
    scheduler = BlockingScheduler()
    scheduler.add_job(
        run_daily_job,
        "cron",
        hour=14,
        minute=0,
        id="daily_fantasy_email",
    )
    print("[scheduler] NBA fantasy job scheduled for 14:00 daily")
    scheduler.start()


def run_now():
    run_daily_job()
    print("[scheduler] Immediate run complete")


if __name__ == "__main__":
    run_now()
