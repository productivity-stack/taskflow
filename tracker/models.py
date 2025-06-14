import uuid
from django.db import models
from django.conf import settings


class Epic(models.Model):
    uid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class TaskStatus(models.TextChoices):
    TODO = "todo", "To Do"
    IN_PROGRESS = "in_progress", "In Progress"
    TEST = "test", "Test"
    DONE = "done", "Done"
    CLOSED = "closed", "Closed"


class TaskPriority(models.TextChoices):
    LOW = "low", "Low"
    MEDIUM = "medium", "Medium"
    HIGH = "high", "High"
    CRITICAL = "critical", "Critical"


class Task(models.Model):
    uid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=TaskStatus.choices,
        default=TaskStatus.TODO,
    )
    priority = models.CharField(
        max_length=10,
        choices=TaskPriority.choices,
        default=TaskPriority.MEDIUM,
    )

    due_date = models.DateTimeField(null=False, blank=False)
    reminder_at = models.DateTimeField(null=True, blank=True)

    epic = models.ForeignKey(
        Epic,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)ss",
    )

    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="created_%(class)ss",
    )
    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="assigned_%(class)ss",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
