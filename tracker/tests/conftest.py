import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.test import APIClient
from tracker.models import Task, TaskStatus

User = get_user_model()


@pytest.fixture
def user(db):
    return User.objects.create_user(
        username="testuser",
        password="testpass",
        email="shr.farahzad@gmail.com",
    )


@pytest.fixture
def another_user(db):
    return User.objects.create_user(
        username="assignee",
        password="assigneepass",
        email="assignee@example.com",
    )


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticated_api_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def task_status_objects(db, user, another_user):
    tasks = {}
    for status in TaskStatus:
        tasks[status] = Task.objects.create(
            title=f"Task {status}",
            status=status,
            due_date=timezone.now() + timezone.timedelta(days=1),
            creator=user,
            assignee=another_user,
        )
    return tasks
