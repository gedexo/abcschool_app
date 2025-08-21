from core.base import BaseTable
from django_tables2 import columns

from .models import Exam, Series, StudentExam


class SeriesTable(BaseTable):
    class Meta:
        model = Series
        fields = (
            "name",
            "description",
        )
        attrs = {"class": "table border-0 star-student table-hover "}


class ExamTable(BaseTable):
    class Meta:
        model = Exam
        fields = (
            "series",
            "subject",
            "date",
            "duration_minutes",
            "max_marks",
            "pass_marks",
        )
        attrs = {"class": "table border-0 star-student table-hover "}


class StudentExamTable(BaseTable):
    marks_obtained = columns.TemplateColumn(template_name="app/partials/marks_obtained_form.html")
    status = columns.Column(orderable=False)

    class Meta:
        model = StudentExam
        fields = (
            "exam",
            "exam__date",
            "exam__duration_minutes",
            "student",
            "student__admission_number",
            "exam__max_marks",
            "marks_obtained",
            "status",
        )
        attrs = {"class": "table border-0 star-student table-hover "}
