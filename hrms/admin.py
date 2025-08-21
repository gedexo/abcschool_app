from core.base import BaseAdmin
from django.contrib import admin

from .models import Attendance, LeaveRequest


@admin.register(LeaveRequest)
class LeaveRequestAdmin(BaseAdmin):
    list_display = (
        "employee",
        "leave_type",
        "start_date",
        "end_date",
        "status",
        "is_active",
    )
    list_filter = ("is_active", "leave_type")
    search_fields = (
        "employee__first_name",
        "employee__middile_name",
        "employee__last_name",
    )
    autocomplete_fields = ("employee",)


@admin.register(Attendance)
class AttendanceAdmin(BaseAdmin):
    list_display = ("attendance_recorder", "student", "date", "status", "is_active")
    list_filter = ("is_active", "status")
    search_fields = ("attendance_recorder__first_name", "student__first_name")
    autocomplete_fields = ("attendance_recorder",)
