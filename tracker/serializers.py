from rest_framework import serializers
from .models import Task, Epic, TaskStatus
from django.utils import timezone


class EpicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Epic
        fields = "__all__"

    def validate_status(self, new_status):
        instance = self.instance
        if instance:
            prev_status = instance.status

            if (
                prev_status in [TaskStatus.DONE, TaskStatus.CLOSED]
                and new_status != prev_status
            ):
                raise serializers.ValidationError(
                    "Cannot change status of a completed epic."
                )

            if prev_status == TaskStatus.TEST and new_status == TaskStatus.TODO:
                raise serializers.ValidationError("Cannot move epic from test to todo.")
        return new_status


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"

    def validate_status(self, new_status):
        instance = self.instance
        if instance:
            prev_status = instance.status

            if (
                prev_status in [TaskStatus.DONE, TaskStatus.CLOSED]
                and new_status != prev_status
            ):
                raise serializers.ValidationError(
                    "Cannot change status of a completed task."
                )

            if prev_status == TaskStatus.TEST and new_status == TaskStatus.TODO:
                raise serializers.ValidationError("Cannot move task from test to todo.")
        return new_status

    def validate(self, data):
        instance = self.instance

        due_date = data.get("due_date") or (instance.due_date if instance else None)
        reminder_at = data.get("reminder_at") or (
            instance.reminder_at if instance else None
        )

        if (
            reminder_at
            and due_date
            and reminder_at >= due_date - timezone.timedelta(minutes=30)
        ):
            raise serializers.ValidationError(
                {"reminder_at": "Reminder must be at least 30 minutes before due date."}
            )

        return data
