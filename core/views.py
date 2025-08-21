from datetime import datetime

from accounting.models import Account
from core import mixins
from django.urls import reverse_lazy
from employees.models import Employee
from hrms.models import Attendance
from students.models import AcademicYearStudentFee, Division, Student
from students.tables import StudentTable

from . import tables
from .models import Suggestion


def get_current_academic_year():
    today = datetime.today()
    current_year = today.year
    if today.month < 6:
        current_year -= 1
    start_year = current_year
    end_year = current_year + 1
    return f"{start_year}-{end_year}"


class HomeView(mixins.HybridListView):
    model = Student
    table_class = StudentTable
    permissions = ("management", "teacher", "accountant", "student")
    template_name = "core/home.html"
    filterset_fields = {
        "division__standard": ["exact"],
        "division__name": ["icontains"],
    }

    def get_queryset(self):
        qs = super().get_queryset().filter(is_active=True)
        if self.request.user.usertype == "teacher":
            divisions = Division.objects.filter(tutor=self.request.user.employee)
            qs = qs.filter(division__in=divisions)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_index"] = True
        context["students_count"] = Student.objects.filter(is_active=True).count()
        context["teacher_count"] = Employee.objects.filter(user__usertype="teacher", is_active=True).count()
        context["workers_count"] = Employee.objects.filter(user__usertype="worker", is_active=True).count()
        context["divisions"] = Division.objects.filter(is_active=True)
        context["division_count"] = Division.objects.filter(is_active=True).count()
        context["accounts"] = Account.objects.filter(is_active=True)
        context["now"] = datetime.today()
        context["today_present"] = Attendance.objects.filter(date=datetime.today(), status="present").count()
        context["today_absent"] = Attendance.objects.filter(date=datetime.today(), status="absent").count()
        if self.request.user.usertype == "student":
            student = self.request.user.student
            print(get_current_academic_year()*222)
            student_fee = AcademicYearStudentFee.objects.filter( student=student, academic_year=get_current_academic_year()).first()
            if student_fee:
                context["current_school_fee"] = student_fee.total_fee()
                context["total_paid"] = student_fee.total_receipt()
                context["fee_pending"] = student_fee.pending_fee()
            else:
                context["current_school_fee"] = 0
                context["total_paid"] = 0
                context["fee_pending"] = 0
        if self.request.user.usertype == "teacher":
            my_divisions = Division.objects.filter(tutor=self.request.user.employee)
            context["my_divisions"] = my_divisions
            context["today_present"] = Attendance.objects.filter(
                date=datetime.today(),
                status="present",
                student__division__in=my_divisions,
            ).count()
            context["today_absent"] = Attendance.objects.filter(
                date=datetime.today(),
                status="absent",
                student__division__in=my_divisions,
            ).count()
        return context


class SuggestionListView(mixins.HybridListView):
    model = Suggestion
    table_class = tables.SuggestionTable
    filterset_fields = {"suggested_by": ["exact"]}
    permissions = ("management", "teacher", "student")

    def get_queryset(self):
        if self.request.user.usertype != "management":
            return super().get_queryset().filter(suggested_by=self.request.user)
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Suggestions"
        context["is_suggestions"] = True
        context["can_add"] = mixins.check_access(self.request, ("management", "teacher", "student"))
        context["new_link"] = reverse_lazy("core:suggestion_create")
        return context


class SuggestionDetailView(mixins.HybridDetailView):
    model = Suggestion
    permissions = ("management", "teacher", "student")


class SuggestionCreateView(mixins.HybridCreateView):
    model = Suggestion
    exclude = ("is_active", "creator", "suggested_by")
    permissions = ("management", "teacher", "student")

    def form_valid(self, form):
        form.instance.suggested_by = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Suggestion"
        return context


class SuggestionUpdateView(mixins.HybridUpdateView):
    model = Suggestion
    exclude = ("is_active", "creator", "suggested_by")
    permissions = ("management", "teacher", "student")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Suggestion"
        return context


class SuggestionDeleteView(mixins.HybridDeleteView):
    model = Suggestion
    permissions = ("management", "teacher", "student")
