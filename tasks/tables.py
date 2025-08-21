from core.base import BaseTable
from django_tables2 import columns

from .models import StudentTask, Task


class TaskTable(BaseTable):
    class Meta:
        model = Task
        fields = ("title", "due_date", "assigned_teacher")
        attrs = {"class": "table border-0 star-student table-hover "}


class StudentTaskTable(BaseTable):
    status = columns.TemplateColumn(template_name="app/partials/task_status_form.html")

    class Meta:
        model = StudentTask
        fields = (
            "task__title",
            "task__due_date",
            "student",
            "student__admission_number",
            "status",
            "task__assigned_teacher",
        )
        attrs = {"class": "table border-0 star-student table-hover "}
