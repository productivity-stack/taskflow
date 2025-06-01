from celery import shared_task
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from tracker.models import Task
from utils.email import send_email


@shared_task
def check_reminders():
    now = timezone.now()
    tasks = Task.objects.filter(reminder_at__lte=now, reminder_at__isnull=False)
    for task in tasks:
        send_email(
            subject="Task Reminder",
            body="tracker/email/reminder.html",
            context={"task": task},
            recipient_list=[task.assignee.email],
        )
        task.reminder_at = None
        task.save(update_fields=["reminder_at"])
