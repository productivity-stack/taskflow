from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, EpicViewSet

router = DefaultRouter()
router.register(r"tasks", TaskViewSet)
router.register(r"epics", EpicViewSet)

urlpatterns = router.urls
