import pytest
from django.utils import timezone
from rest_framework.test import APIClient
from tracker.models import Task, TaskStatus


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def task_status_objects(db):
    tasks = {}
    for status in TaskStatus:
        tasks[status] = Task.objects.create(
            title=f"Task {status}",
            status=status,
            due_date=timezone.now() + timezone.timedelta(days=1),
        )
    return tasks
