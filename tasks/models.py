from core.base import BaseModel
from core.choices import TASK_STATUS_CHOICE
from django.db import models
from django.urls import reverse_lazy


class Task(BaseModel):
    title = models.CharField(max_length=100, help_text="Enter the title of the task")
    due_date = models.DateField(help_text="Enter the due date for the task")
    assigned_teacher = models.ForeignKey("employees.Employee", on_delete=models.PROTECT, related_name="assigned_tasks")
    description = models.TextField(null=True, blank=True, help_text="Enter a description for the task")

    class Meta:
        ordering = ["-due_date", "assigned_teacher"]
        unique_together = ("title", "due_date")

    def __str__(self):
        return f"{self.title} - Due Date: {self.due_date}"

    def get_absolute_url(self):
        return reverse_lazy("tasks:task_detail", kwargs={"pk": self.pk})

    @staticmethod
    def get_list_url():
        return reverse_lazy("tasks:task_list")

    def get_update_url(self):
        return reverse_lazy("tasks:task_update", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse_lazy("tasks:task_delete", kwargs={"pk": self.pk})


class StudentTask(BaseModel):
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="task_assignments",
        limit_choices_to={"is_active": True},
    )
    student = models.ForeignKey("students.Student", on_delete=models.PROTECT, related_name="assigned_tasks")
    status = models.CharField(max_length=20, choices=TASK_STATUS_CHOICE, default="assigned")

    class Meta:
        unique_together = ("task", "student")

    def __str__(self):
        return f"Task: {self.task.title} - Assigned to: {self.student}"

    def get_absolute_url(self):
        return reverse_lazy("tasks:student_task_detail", kwargs={"pk": self.pk})

    @staticmethod
    def get_list_url():
        return reverse_lazy("tasks:student_task_list")

    def get_update_url(self):
        return reverse_lazy("tasks:student_task_update", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse_lazy("tasks:student_task_delete", kwargs={"pk": self.pk})
