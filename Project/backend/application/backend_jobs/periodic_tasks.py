from application.backend_jobs.celery_system import celery
from celery.schedules import crontab
from application.backend_jobs.task_reminder_checker import task_reminder
from application.backend_jobs.monthly_report import monthly_report

@celery.on_after_configure.connect()
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(hour=21, minute=00),task_reminder.s(),name='daily reminder')
    sender.add_periodic_task(crontab(hour=21, minute=15, day_of_month=1),monthly_report.s(),name='monthly report')
