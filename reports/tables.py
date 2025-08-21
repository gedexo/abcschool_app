from core.base import BaseTable
from django_tables2 import columns
from students.models import AcademicYearStudentFee

from .functions import get_due_fee, get_fee, monthly_student_fee_receipt


class StudentMasterTable(BaseTable):
    total_fee = columns.Column(orderable=False)
    uniform_fee = columns.Column(empty_values=(), orderable=False)
    book_fee = columns.Column(empty_values=(), orderable=False)
    worksheet_fee = columns.Column(empty_values=(), orderable=False)
    other_fee = columns.Column(empty_values=(), orderable=False)

    july_fee = columns.Column(empty_values=(), orderable=False)
    august_fee = columns.Column(empty_values=(), orderable=False)
    september_fee = columns.Column(empty_values=(), orderable=False)
    october_fee = columns.Column(empty_values=(), orderable=False)
    november_fee = columns.Column(empty_values=(), orderable=False)
    december_fee = columns.Column(empty_values=(), orderable=False)
    january_fee = columns.Column(empty_values=(), orderable=False)
    february_fee = columns.Column(empty_values=(), orderable=False)

    july_fee_due = columns.Column(empty_values=(), orderable=False)
    august_fee_due = columns.Column(empty_values=(), orderable=False)
    september_fee_due = columns.Column(empty_values=(), orderable=False)
    october_fee_due = columns.Column(empty_values=(), orderable=False)
    november_fee_due = columns.Column(empty_values=(), orderable=False)
    december_fee_due = columns.Column(empty_values=(), orderable=False)
    january_fee_due = columns.Column(empty_values=(), orderable=False)
    february_fee_due = columns.Column(empty_values=(), orderable=False)

    total_due_fee = columns.Column(empty_values=(), orderable=False)

    admission_fee_receipt = columns.Column(empty_values=(), orderable=False)

    july_fee_receipt = columns.Column(empty_values=(), orderable=False)
    august_fee_receipt = columns.Column(empty_values=(), orderable=False)
    september_fee_receipt = columns.Column(empty_values=(), orderable=False)
    october_fee_receipt = columns.Column(empty_values=(), orderable=False)
    november_fee_receipt = columns.Column(empty_values=(), orderable=False)
    december_fee_receipt = columns.Column(empty_values=(), orderable=False)
    january_fee_receipt = columns.Column(empty_values=(), orderable=False)
    february_fee_receipt = columns.Column(empty_values=(), orderable=False)
    total_receipt = columns.Column(orderable=False)
    out_standing_fee = columns.Column(empty_values=(), orderable=False)
    action = None
    created = None

    def render_book_fee(self, value, record):
        return get_fee(record, "book_fee")

    def render_worksheet_fee(self, value, record):
        return get_fee(record, "book_fee")

    def render_uniform_fee(self, value, record):
        return get_fee(record, "uniform_fee")

    def render_other_fee(self, value, record):
        return get_fee(record, "other_fee")

    def render_july_fee(self, value, record):
        return record.generate_fee_structure()[0]["fee"]

    def render_august_fee(self, value, record):
        return record.generate_fee_structure()[1]["fee"]

    def render_september_fee(self, value, record):
        return record.generate_fee_structure()[2]["fee"]

    def render_october_fee(self, value, record):
        return record.generate_fee_structure()[3]["fee"]

    def render_november_fee(self, value, record):
        return record.generate_fee_structure()[4]["fee"]

    def render_december_fee(self, value, record):
        return record.generate_fee_structure()[5]["fee"]

    def render_january_fee(self, value, record):
        return record.generate_fee_structure()[6]["fee"]

    def render_february_fee(self, value, record):
        return record.generate_fee_structure()[7]["fee"]

    def render_july_fee_due(self, value, record):
        return get_due_fee(record, "July")

    def render_august_fee_due(self, value, record):
        return get_due_fee(record, "August")

    def render_september_fee_due(self, value, record):
        return get_due_fee(record, "September")

    def render_october_fee_due(self, value, record):
        return get_due_fee(record, "October")

    def render_november_fee_due(self, value, record):
        return get_due_fee(record, "November")

    def render_december_fee_due(self, value, record):
        return get_due_fee(record, "December")

    def render_january_fee_due(self, value, record):
        return get_due_fee(record, "January")

    def render_february_fee_due(self, value, record):
        return get_due_fee(record, "February")

    def render_total_due_fee(self, value, record):
        july_due = get_due_fee(record, "July")
        august_due = get_due_fee(record, "August")
        september_due = get_due_fee(record, "September")
        october_due = get_due_fee(record, "October")
        november_due = get_due_fee(record, "November")
        december_due = get_due_fee(record, "December")
        january_due = get_due_fee(record, "January")
        february_due = get_due_fee(record, "February")
        total_due_fee = july_due + august_due + september_due + october_due + november_due + december_due + january_due + february_due + record.donation_fee

        return total_due_fee

    def render_admission_fee_receipt(self, value, record):
        return monthly_student_fee_receipt(record, 6)

    def render_july_fee_receipt(self, value, record):
        return monthly_student_fee_receipt(record, 7)

    def render_august_fee_receipt(self, value, record):
        return monthly_student_fee_receipt(record, 8)

    def render_september_fee_receipt(self, value, record):
        return monthly_student_fee_receipt(record, 9)

    def render_october_fee_receipt(self, value, record):
        return monthly_student_fee_receipt(record, 10)

    def render_november_fee_receipt(self, value, record):
        return monthly_student_fee_receipt(record, 11)

    def render_december_fee_receipt(self, value, record):
        return monthly_student_fee_receipt(record, 12)

    def render_january_fee_receipt(self, value, record):
        return monthly_student_fee_receipt(record, 1)

    def render_february_fee_receipt(self, value, record):
        return monthly_student_fee_receipt(record, 2)

    def render_out_standing_fee(self, value, record):
        return self.render_total_due_fee(value, record) - record.total_receipt()

    class Meta:
        model = AcademicYearStudentFee
        fields = (
            "student__admission_number",
            "student",
            "student__division__standard",
            "student__division__name",
            "school_fee",
            "donation_fee",
            "july_fee",
            "august_fee",
            "september_fee",
            "october_fee",
            "november_fee",
            "december_fee",
            "january_fee",
            "february_fee",
            "uniform_fee",
            "book_fee",
            "worksheet_fee",
            "other_fee",
            "total_fee",
        )
        attrs = {"class": "table border-0 star-student table-hover "}
