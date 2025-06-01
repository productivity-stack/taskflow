from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Task, Epic
from .serializers import TaskSerializer, EpicSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all().order_by("-created_at")
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class EpicViewSet(viewsets.ModelViewSet):
    queryset = Epic.objects.all().order_by("-created_at")
    serializer_class = EpicSerializer
    permission_classes = [IsAuthenticated]
