from core import mixins
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from exams.forms import ExamForm

from . import tables
from .models import Exam, Series, StudentExam


class SeriesListView(mixins.HybridListView):
    model = Series
    table_class = tables.SeriesTable
    filterset_fields = {"name": ["icontains"]}
    permissions = ("management", "teacher")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Exam Types"
        context["is_series"] = True
        context["can_add"] = mixins.check_access(self.request, ("management", "teacher"))
        context["new_link"] = reverse_lazy("exams:series_create")
        return context


class SeriesDetailView(mixins.HybridDetailView):
    model = Series
    permissions = ("management", "teacher")


class SeriesCreateView(mixins.HybridCreateView):
    model = Series
    permissions = ("management", "teacher")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Series"
        return context


class SeriesUpdateView(mixins.HybridUpdateView):
    model = Series
    permissions = ("management", "teacher")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Series"
        return context


class SeriesDeleteView(mixins.HybridDeleteView):
    model = Series
    permissions = ("management", "teacher")


class ExamListView(mixins.HybridListView):
    model = Exam
    table_class = tables.ExamTable
    filterset_fields = {
        "series": ["exact"],
        "subject": ["icontains"],
        "date": ["lte"],
    }
    permissions = ("management", "teacher", "student")

    def get_queryset(self):
        base_qs = super().get_queryset()
        if self.request.user.usertype == "student":
            base_qs = base_qs.filter(division=self.request.user.student.division)
        return base_qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Exam"
        context["is_exams"] = True
        context["can_add"] = mixins.check_access(self.request, ("management", "teacher"))
        context["new_link"] = reverse_lazy("exams:exam_create")
        return context


class ExamDetailView(mixins.HybridDetailView):
    model = Exam
    permissions = ("management", "teacher", "student")


class ExamCreateView(mixins.CustomLoginRequiredMixin, mixins.CreateView):
    model = Exam
    permissions = ("management", "teacher")
    form_class = ExamForm
    template_name = "app/common/object_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Exam"
        return context


class ExamUpdateView(mixins.HybridUpdateView):
    model = Exam
    permissions = ("management", "teacher")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Exam"
        return context


class ExamDeleteView(mixins.HybridDeleteView):
    model = Exam
    permissions = ("management", "teacher")


class StudentExamListView(mixins.HybridListView):
    model = StudentExam
    table_class = tables.StudentExamTable
    filterset_fields = {
        "exam__series": ["exact"],
        "exam__subject": ["icontains"],
        "student__division__standard": ["exact"],
    }
    permissions = ("management", "teacher", "student")
    template_name = "exams/student_exam_filter.html"

    def get_queryset(self):
        base_qs = super().get_queryset()
        if self.request.user.usertype == "student":
            base_qs = base_qs.filter(student=self.request.user.student)
        return base_qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Exam Results"
        context["is_student_exams"] = True
        context["can_add"] = mixins.check_access(self.request, ("management", "teacher"))
        context["new_link"] = reverse_lazy("exams:student_exam_create")
        return context


class StudentExamDetailView(mixins.HybridDetailView):
    model = StudentExam
    permissions = ("management", "teacher", "student")


class StudentExamCreateView(mixins.HybridCreateView):
    model = StudentExam
    permissions = ("management", "teacher")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Exam Result"
        return context


class StudentExamUpdateView(mixins.HybridUpdateView):
    model = StudentExam
    permissions = ("management", "teacher")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Exam Result"
        return context


class StudentExamDeleteView(mixins.HybridDeleteView):
    model = StudentExam
    permissions = ("management", "teacher")


def student_mark_update(request, pk):
    print("ujdfgdj")
    obtained_mark = request.POST.get("marks_obtained")
    student_obj = get_object_or_404(StudentExam, pk=pk)
    student_obj.marks_obtained = obtained_mark
    student_obj.is_marked = True
    student_obj.save()
    return JsonResponse({"status": "success"})
