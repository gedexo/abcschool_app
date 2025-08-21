from core.base import BaseAdmin
from django.contrib import admin

from .models import StudentTask, Task


@admin.register(Task)
class TaskAdmin(BaseAdmin):
    list_display = ("title", "due_date", "assigned_teacher")
    list_filter = ("due_date",)
    search_fields = ("assigned_teacher__first_name",)


@admin.register(StudentTask)
class StudentTaskAdmin(BaseAdmin):
    list_display = ("task", "student", "status")
    list_filter = ("status",)
    search_fields = ("student__first_name",)
