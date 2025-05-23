from rest_framework import viewsets
from .models import Task, Epic
from .serializers import TaskSerializer, EpicSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all().order_by("-created_at")
    serializer_class = TaskSerializer


class EpicViewSet(viewsets.ModelViewSet):
    queryset = Epic.objects.all().order_by("-created_at")
    serializer_class = EpicSerializer
