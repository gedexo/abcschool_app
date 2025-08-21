from core.base import BaseAdmin
from django.contrib import admin

from .models import Exam, Series, StudentExam


@admin.register(Series)
class SeriesAdmin(BaseAdmin):
    list_display = ("name", "description")
    list_filter = ("name",)
    search_fields = ("name",)


@admin.register(Exam)
class ExamAdmin(BaseAdmin):
    list_display = ("series", "subject", "date", "max_marks", "pass_marks")
    list_filter = ("date",)
    search_fields = ("series__name",)


@admin.register(StudentExam)
class StudentExamAdmin(BaseAdmin):
    list_display = ("exam", "student", "marks_obtained")
    search_fields = ("student__first_name",)
