from core.base import BaseAdmin
from django.contrib import admin

from .models import (
    AcademicYearStudentFee,
    Division,
    Standard,
    Student,
    StudentFeeStatement,
)


@admin.register(Standard)
class StandardAdmin(BaseAdmin):
    list_display = (
        "name",
        "description",
    )
    list_filter = ("is_active",)
    search_fields = ("name",)


@admin.register(Division)
class DivisionAdmin(BaseAdmin):
    list_display = (
        "name",
        "description",
    )
    list_filter = ("is_active",)
    search_fields = ("name",)


@admin.register(Student)
class StudentAdmin(BaseAdmin):
    list_display = (
        "admission_number",
        "first_name",
        "last_name",
        "gender",
        "date_of_birth",
    )
    list_filter = (
        "gender",
        "blood_group",
    )
    search_fields = ("admission_number", "first_name", "last_name", "email")


@admin.register(AcademicYearStudentFee)
class AcademicYearStudentFeeAdmin(BaseAdmin):
    list_display = ("academic_year", "student", "school_fee", "donation_fee")
    list_filter = ("academic_year",)
    search_fields = ("student__first_name",)


@admin.register(StudentFeeStatement)
class StudentFeeStatementAdmin(BaseAdmin):
    list_display = ("student", "amount", "account", "date", "voucher_number")
    list_filter = ("account",)
    search_fields = ("student__first_name",)
