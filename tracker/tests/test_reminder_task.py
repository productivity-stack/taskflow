from unittest.mock import patch
import pytest
from django.utils import timezone
from tracker.models import Task
from utils.tasks import check_reminders
from django.contrib.auth import get_user_model
from datetime import timedelta


User = get_user_model()


@pytest.mark.django_db
@patch("utils.tasks.send_email")
def test_send_email_called(mock_send_email):
    # user = User.objects.create_user(
    #     username="testuser", email="test@example.com", password="pass"
    # )

    task = Task.objects.create(
        title="Test Task",
        description="Some Description",
        due_date=timezone.now() + timedelta(minutes=35),
        reminder_at=timezone.now() - timedelta(seconds=10),
        # user=user,
    )

    check_reminders()

    assert mock_send_email.called
    mock_send_email.assert_called_with(
        subject="Task Reminder",
        body="tracker/email/reminder.html",
        context={"task": task},
        recipient_list=["shr.farahzad@gmail.com"],
    )


@pytest.mark.django_db
@patch("utils.tasks.send_email")
def test_do_not_send_email_if_reminder_time_in_future(mock_send_email):
    # user = User.objects.create_user(
    #     username="testuser2", email="future@example.com", password="pass"
    # )
    task = Task.objects.create(
        title="Future Task",
        description="Future Desc",
        due_date=timezone.now() + timezone.timedelta(minutes=35),
        reminder_at=timezone.now() + timezone.timedelta(minutes=5),
        # user=user,
    )

    check_reminders()

    assert not mock_send_email.called
