import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "taskflow.settings")

app = Celery("taskflow", broker="redis://redis:6379/0")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


app.conf.beat_schedule = {
    "check-reminder_at": {
        "task": "utils.tasks.check_reminders",
        "schedule": crontab(minute="*/1"),
    },
}
