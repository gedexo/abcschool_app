from core.base import BaseModel
from core.choices import (
    ATTENDANCE_STATUS_CHOICES,
    LEAVE_STATUS_CHOICE,
    LEAVE_TYPE_CHOICES,
)
from django.db import models
from django.urls import reverse_lazy
from django.utils import timezone


class LeaveRequest(BaseModel):
    employee = models.ForeignKey("employees.Employee", on_delete=models.CASCADE)
    leave_type = models.CharField(max_length=25, choices=LEAVE_TYPE_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    remarks = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=LEAVE_STATUS_CHOICE, default="pending")

    @staticmethod
    def get_list_url():
        return reverse_lazy("hrms:leave_request_list")

    def get_absolute_url(self):
        return reverse_lazy("hrms:leave_request_detail", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse_lazy("hrms:leave_request_update", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse_lazy("hrms:leave_request_delete", kwargs={"pk": self.pk})

    def __str__(self):
        return f"{self.employee} Leave Request"


class Attendance(BaseModel):
    attendance_recorder = models.ForeignKey(
        "employees.Employee",
        on_delete=models.PROTECT,
        limit_choices_to={
            "user__usertype__in": (
                "teacher",
                "management",
            )
        },
    )
    student = models.ForeignKey("students.Student", on_delete=models.PROTECT)
    date = models.DateField(default=timezone.localdate)
    status = models.CharField(max_length=20, default="present", choices=ATTENDANCE_STATUS_CHOICES)

    class Meta:
        ordering = ("-date",)
        unique_together = ("student", "date")

    @staticmethod
    def get_list_url():
        return reverse_lazy("hrms:attendance_list")

    def get_absolute_url(self):
        return reverse_lazy("hrms:attendance_detail", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse_lazy("hrms:attendance_delete", kwargs={"pk": self.pk})

    def __str__(self):
        return f"{self.student} Attendence"
