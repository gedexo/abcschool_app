from core.base import BaseAdmin
from django.contrib import admin

from .models import Department, Designation, Employee, EmployeePayment, EmployeePayroll


@admin.register(Designation)
class DesignationAdmin(BaseAdmin):
    list_display = ("name", "description")
    list_filter = ("name",)
    search_fields = ("name",)


@admin.register(Department)
class DepartmentAdmin(BaseAdmin):
    list_display = ("name", "description")
    list_filter = ("name",)
    search_fields = ("name", "description")


@admin.register(Employee)
class EmployeeAdmin(BaseAdmin):
    list_display = ("employee_id", "fullname", "gender")
    list_filter = ("gender",)
    search_fields = ("employee_id", "first_name", "last_name")


@admin.register(EmployeePayroll)
class EmployeePayrollAdmin(BaseAdmin):
    list_display = ("employee", "amount", "month", "year")
    list_filter = ("month", "year")  # Add more filter fields as needed
    search_fields = ("employee__name",)


@admin.register(EmployeePayment)
class EmployeePaymentAdmin(BaseAdmin):
    list_display = ("employee", "amount", "date")
    list_filter = ("date", "is_active")
    search_fields = ("employee__first_name",)
