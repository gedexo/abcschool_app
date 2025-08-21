from core.base import BaseTable
from django_tables2 import columns

from .models import (
    AcademicYearStudentFee,
    Division,
    Standard,
    Student,
    StudentFeeStatement,
)


class StudentTable(BaseTable):
    fullname = columns.Column(linkify=True, verbose_name="Name", order_by="first_name")
    division__name = columns.Column(verbose_name="Division")
    primary_contact_number = columns.TemplateColumn(
        """
        {% if record.primary_contact_number %}
            <a href="tel:+91{{ record.primary_contact_number }}">{{ record.primary_contact_number }}</a>
        {% endif  %}
        """
    )
    created = None

    class Meta:
        model = Student
        fields = (
            "admission_number",
            "fullname",
            "division__standard",
            "division__name",
            "bus_no",
            "primary_contact_number",
        )
        attrs = {"class": "table border-0 star-student table-hover "}


class StudentFeeStatementTable(BaseTable):
    class Meta:
        model = StudentFeeStatement
        fields = (
            "academic_year",
            "student",
            "account",
            "amount",
            "date",
            "voucher_number",
        )
        attrs = {"class": "table border-0 star-student table-hover "}


class AcademicYearStudentFeeTable(BaseTable):
    class Meta:
        model = AcademicYearStudentFee
        fields = (
            "academic_year",
            "student__admission_number",
            "student",
            "school_fee",
            "donation_fee",
        )
        attrs = {"class": "table border-0 star-student table-hover "}


class StandardTable(BaseTable):
    class Meta:
        model = Standard
        fields = ("name",)
        attrs = {"class": "table border-0 star-student table-hover "}


class DivisionTable(BaseTable):
    class Meta:
        model = Division
        fields = ("standard", "name", "tutor")
        attrs = {"class": "table border-0 star-student table-hover "}
