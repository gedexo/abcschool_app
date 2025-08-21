from core.base import BaseTable
from django_tables2 import columns

from .models import Department, Designation, Employee, EmployeePayment, EmployeePayroll


class EmployeeTable(BaseTable):
    fullname = columns.Column(linkify=True, orderable=False)

    class Meta:
        model = Employee
        fields = ("employee_id", "fullname", "department", "designation", "is_active")
        attrs = {"class": "table border-0 star-student table-hover "}


class DepartmentTable(BaseTable):
    class Meta:
        model = Department
        fields = ("name", "department_lead", "is_active")
        attrs = {"class": "table border-0 star-student table-hover "}


class DesignationTable(BaseTable):
    class Meta:
        model = Designation
        fields = ("name", "is_active")
        attrs = {"class": "table border-0 star-student table-hover "}


class EmployeePayrollTable(BaseTable):
    employee = columns.Column(linkify=True)

    class Meta:
        model = EmployeePayroll
        fields = ("employee", "month", "year", "amount")
        attrs = {"class": "table border-0 star-student table-hover "}


class EmployeePaymentTable(BaseTable):
    class Meta:
        model = EmployeePayment
        fields = ("employee", "account", "amount", "date", "voucher_number")
        attrs = {"class": "table border-0 star-student table-hover "}
