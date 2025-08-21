from core.base import BaseTable
from django_tables2 import columns

from .models import AdditionalFeeStudent


class AdditionalFeeStudentTable(BaseTable):
    get_fee_name = columns.Column(verbose_name="Fee")

    class Meta:
        model = AdditionalFeeStudent
        fields = (
            "academic_year",
            "get_fee_name",
            "student__admission_number",
            "student",
            "amount",
            "due_date",
        )
        attrs = {"class": "table border-0 star-student table-hover "}
