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
    print("Scheduler started at 14:00.")
    scheduler.start()
