from django.contrib import admin
from .models import Epic, Task


class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "epic", "due_date", "created_at")
    list_filter = ("status", "due_date", "epic")
    search_fields = ("title", "description")
    ordering = ("-due_date",)
    list_per_page = 20


class EpicAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at")
    search_fields = ("title",)
    ordering = ("-created_at",)


admin.site.register(Task, TaskAdmin)
admin.site.register(Epic, EpicAdmin)
