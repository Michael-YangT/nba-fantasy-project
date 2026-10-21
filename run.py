from app.jobs.run_daily import run_daily_job
from app.notifications.scheduler import start_scheduler

if __name__ == "__main__":
    run_daily_job()
    # Uncomment to enable daily scheduler at 14:00
    # start_scheduler()
