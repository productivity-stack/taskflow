import pytest
from django.utils import timezone
from tracker.serializers import TaskSerializer
from tracker.models import Task, TaskStatus


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("from_status", "to_status"),
    [
        (TaskStatus.DONE, TaskStatus.TODO),
        (TaskStatus.DONE, TaskStatus.IN_PROGRESS),
        (TaskStatus.DONE, TaskStatus.TEST),
        (TaskStatus.CLOSED, TaskStatus.TODO),
        (TaskStatus.CLOSED, TaskStatus.IN_PROGRESS),
        (TaskStatus.CLOSED, TaskStatus.TEST),
        (TaskStatus.CLOSED, TaskStatus.DONE),
    ],
)
def test_forbidden_task_status_transitions(task_status_objects, from_status, to_status):
    task = task_status_objects[from_status]
    serializer = TaskSerializer(instance=task, data={"status": to_status}, partial=True)

    assert (
        not serializer.is_valid()
    ), f"Transition from {from_status} to {to_status} should be invalid"
    assert "status" in serializer.errors


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("from_status", "to_status"),
    [
        (TaskStatus.TODO, TaskStatus.IN_PROGRESS),
        (TaskStatus.TODO, TaskStatus.TEST),
        (TaskStatus.TODO, TaskStatus.DONE),
        (TaskStatus.TODO, TaskStatus.CLOSED),
        (TaskStatus.IN_PROGRESS, TaskStatus.TODO),
        (TaskStatus.IN_PROGRESS, TaskStatus.TEST),
        (TaskStatus.IN_PROGRESS, TaskStatus.DONE),
        (TaskStatus.IN_PROGRESS, TaskStatus.CLOSED),
        (TaskStatus.TEST, TaskStatus.TODO),
        (TaskStatus.TEST, TaskStatus.IN_PROGRESS),
        (TaskStatus.TEST, TaskStatus.DONE),
        (TaskStatus.TEST, TaskStatus.CLOSED),
        (TaskStatus.DONE, TaskStatus.CLOSED),
    ],
)
def test_allowed_task_status_transitions(task_status_objects, from_status, to_status):
    task = task_status_objects[from_status]
    serializer = TaskSerializer(instance=task, data={"status": to_status}, partial=True)

    assert (
        serializer.is_valid()
    ), f"Transition from {from_status} to {to_status} should be valid"
    serializer.save()
    task.refresh_from_db()
    assert task.status == to_status


@pytest.mark.django_db
@pytest.mark.parametrize(
    "minutes_from_now, should_be_valid",
    [
        (-10, False),
        (10, False),
        (35, True),
        (60, True),
    ],
)
def test_due_date_validation(user, another_user, minutes_from_now, should_be_valid):
    due_date = timezone.now() + timezone.timedelta(minutes=minutes_from_now)
    task = Task.objects.create(
        title="Test Task",
        status=TaskStatus.TODO,
        due_date=timezone.now() + timezone.timedelta(minutes=60),
        creator=user,
        assignee=another_user,
    )

    serializer = TaskSerializer(
        instance=task,
        data={"due_date": due_date},
        partial=True,
    )

    is_valid = serializer.is_valid()

    if should_be_valid:
        assert is_valid, f"Due date {minutes_from_now} min from now should be valid"
    else:
        assert (
            not is_valid
        ), f"Due date {minutes_from_now} min from now should be invalid"
        assert "due_date" in serializer.errors


@pytest.mark.django_db
@pytest.mark.parametrize(
    "minutes_before_due, should_be_valid",
    [
        (25, False),
        (30, True),
        (35, True),
        (41, False),
    ],
)
def test_reminder_time_validation_relative_to_due_date(
    user, another_user, minutes_before_due, should_be_valid
):
    due_date = timezone.now() + timezone.timedelta(minutes=40)
    reminder_at = due_date - timezone.timedelta(minutes=minutes_before_due)

    task = Task.objects.create(
        title="Test Task",
        status=TaskStatus.TODO,
        due_date=due_date,
        creator=user,
        assignee=another_user,
    )

    serializer = TaskSerializer(
        instance=task,
        data={"due_date": due_date, "reminder_at": reminder_at},
        partial=True,
    )

    is_valid = serializer.is_valid()

    if should_be_valid:
        assert (
            is_valid
        ), f"Reminder {minutes_before_due} minutes before due date should be valid"
    else:
        assert (
            not is_valid
        ), f"Reminder {minutes_before_due} minutes before due date should be invalid"
        assert "reminder_at" in serializer.errors


@pytest.mark.django_db
def test_due_date_is_required(user, another_user):
    serializer = TaskSerializer(
        data={
            "title": "Task with no due date",
            "status": TaskStatus.TODO,
            "reminder_at": timezone.now() + timezone.timedelta(minutes=10),
            "creator": user.id,
            "assignee": another_user.id,
        }
    )

    is_valid = serializer.is_valid()

    assert not is_valid, "Task without due_date should be invalid"
    assert "due_date" in serializer.errors
