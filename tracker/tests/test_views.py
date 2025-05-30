import pytest
from django.urls import reverse
from django.utils import timezone
from tracker.models import TaskStatus


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
def test_forbidden_status_transitions_view(
    api_client, task_status_objects, from_status, to_status
):
    task = task_status_objects[from_status]
    url = reverse("task-detail", kwargs={"pk": task.pk})

    response = api_client.patch(url, data={"status": to_status}, format="json")
    assert response.status_code == 400
    assert "status" in response.json()


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
def test_allowed_status_transitions_view(
    api_client, task_status_objects, from_status, to_status
):
    task = task_status_objects[from_status]
    url = reverse("task-detail", kwargs={"pk": task.pk})

    response = api_client.patch(url, data={"status": to_status}, format="json")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == to_status


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
def test_due_date_validation_view(api_client, minutes_from_now, should_be_valid):
    due_date = (
        timezone.now() + timezone.timedelta(minutes=minutes_from_now)
    ).isoformat()
    url = reverse("task-list")

    data = {
        "title": "New Task",
        "status": TaskStatus.TODO,
        "due_date": due_date,
    }
    response = api_client.post(url, data=data, format="json")

    if should_be_valid:
        assert response.status_code in (200, 201)
    else:
        assert response.status_code == 400
        assert "due_date" in response.json()


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
def test_reminder_time_validation_view(api_client, minutes_before_due, should_be_valid):
    due_date = timezone.now() + timezone.timedelta(minutes=40)
    reminder_at = due_date - timezone.timedelta(minutes=minutes_before_due)
    due_date_str = due_date.isoformat()
    reminder_str = reminder_at.isoformat()

    url = reverse("task-list")

    data = {
        "title": "Task with reminder",
        "status": TaskStatus.TODO,
        "due_date": due_date_str,
        "reminder_at": reminder_str,
    }
    response = api_client.post(url, data=data, format="json")

    if should_be_valid:
        assert response.status_code in (200, 201)
    else:
        assert response.status_code == 400
        assert "reminder_at" in response.json()


@pytest.mark.django_db
def test_due_date_is_required_view(api_client):
    url = reverse("task-list")

    data = {
        "title": "Task without due date",
        "status": TaskStatus.TODO,
    }

    response = api_client.post(url, data=data, format="json")

    assert response.status_code == 400
    assert "due_date" in response.json()
