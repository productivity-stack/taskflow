from rest_framework import serializers
from .models import Task, Epic, TaskStatus
from django.utils import timezone


class EpicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Epic
        fields = "__all__"


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"

    def validate_status(self, new_status):
        instance = self.instance
        if instance:
            prev_status = instance.status

            if prev_status == TaskStatus.CLOSED and new_status != prev_status:
                raise serializers.ValidationError(
                    "Cannot change status of a closed task."
                )

            if prev_status == TaskStatus.DONE and new_status not in [
                TaskStatus.DONE,
                TaskStatus.CLOSED,
            ]:
                raise serializers.ValidationError(
                    "Cannot revert from done to a previous status."
                )

        return new_status

    def validate_due_date(self, due_date):
        if due_date and due_date < timezone.now() + timezone.timedelta(minutes=30):
            raise serializers.ValidationError(
                "Due date must be at least 30 minutes in the future."
            )
        return due_date

    def validate(self, data):
        instance = self.instance

        due_date = data.get("due_date") or (instance.due_date if instance else None)
        reminder_at = data.get("reminder_at") or (
            instance.reminder_at if instance else None
        )

        if reminder_at:
            if reminder_at < timezone.now():
                raise serializers.ValidationError(
                    {"reminder_at": "Reminder must be in the future."}
                )
            if due_date and reminder_at > due_date - timezone.timedelta(minutes=30):
                raise serializers.ValidationError(
                    {
                        "reminder_at": "Reminder must be at least 30 minutes before due date."
                    }
                )

        return data
