import pytest
from django.utils import timezone
from django.contrib.auth import get_user_model
from tracker.models import Epic, Task, TaskStatus, TaskPriority

User = get_user_model()


@pytest.mark.django_db
def test_create_epic():
    epic = Epic.objects.create(title="Test Epic", description="Epic desc")
    assert epic.pk is not None
    assert epic.title == "Test Epic"
    assert str(epic) == "Test Epic"


@pytest.mark.django_db
def test_create_task():
    creator = User.objects.create_user(username="creator", password="testpass")
    assignee = User.objects.create_user(username="assignee", password="testpass")
    due_date = timezone.now() + timezone.timedelta(days=1)
    task = Task.objects.create(
        title="Test Task",
        due_date=due_date,
        creator=creator,
        assignee=assignee,
    )
    assert task.pk is not None
    assert task.status == TaskStatus.TODO
    assert task.priority == TaskPriority.MEDIUM
    assert task.creator == creator
    assert task.assignee == assignee
    assert str(task) == "Test Task"


@pytest.mark.django_db
def test_task_with_all_fields():
    creator = User.objects.create_user(username="creator2", password="testpass2")
    assignee = User.objects.create_user(username="assignee2", password="testpass2")
    epic = Epic.objects.create(title="Epic 1")
    due_date = timezone.now() + timezone.timedelta(days=2)
    reminder_at = timezone.now() + timezone.timedelta(days=1)
    task = Task.objects.create(
        title="Full Task",
        description="Some description",
        status=TaskStatus.IN_PROGRESS,
        priority=TaskPriority.HIGH,
        due_date=due_date,
        reminder_at=reminder_at,
        epic=epic,
        creator=creator,
        assignee=assignee,
    )
    assert task.status == TaskStatus.IN_PROGRESS
    assert task.priority == TaskPriority.HIGH
    assert task.epic == epic
    assert task.creator == creator
    assert task.assignee == assignee
    assert str(task) == "Full Task"


@pytest.mark.django_db
def test_task_requires_due_date():
    creator = User.objects.create_user(username="creator3", password="testpass3")
    assignee = User.objects.create_user(username="assignee3", password="testpass3")
    with pytest.raises(Exception):
        Task.objects.create(
            title="No due date task",
            creator=creator,
            assignee=assignee,
        )
