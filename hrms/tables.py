from core.base import BaseTable
from django_tables2 import columns

from .models import Attendance, LeaveRequest


class LeaveRequestTable(BaseTable):
    employee = columns.Column(linkify=True)
    status = columns.TemplateColumn(template_name="app/partials/leave_request_status_form.html")

    class Meta:
        model = LeaveRequest
        fields = (
            "employee",
            "leave_type",
            "start_date",
            "end_date",
            "reason",
            "status",
        )
        attrs = {"class": "table border-0 star-student table-hover "}


class AttendanceTable(BaseTable):
    student = columns.Column(linkify=True)
    status = columns.TemplateColumn(template_name="app/partials/attendence_status_form.html")
    student__division = columns.Column(verbose_name="Class")

    class Meta:
        model = Attendance
        fields = (
            "student",
            "student__admission_number",
            "student__division",
            "date",
            "status",
            "attendance_recorder",
        )
        attrs = {"class": "table border-0 star-student table-hover"}
