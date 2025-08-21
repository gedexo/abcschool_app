from accounts.models import User
from core import mixins
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy

from . import tables
from .models import (
    AcademicYearStudentFee,
    Division,
    Standard,
    Student,
    StudentFeeStatement,
)


class StudentListView(mixins.HybridListView):
    model = Student
    table_class = tables.StudentTable
    filterset_fields = {
        "first_name": ["icontains"],
        "admission_number": ["icontains"],
        "division__standard": ["exact"],
        "division__name": ["icontains"],
    }
    permissions = ("management", "teacher", "branch", "accountant")

    def get_queryset(self):
        base_queryset = self.model.objects.filter(is_active=True)
        user_type = self.request.user.usertype
        if user_type == "branch":
            base_queryset = base_queryset.filter(batch__branch__user=self.request.user)
        return base_queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Students"
        context["is_student"] = True
        context["can_add"] = mixins.check_access(self.request, ("management", "teacher", "branch", "accountant"))
        context["can_fee_add"] = mixins.check_access(self.request, ("accountant",))
        context["new_link"] = reverse_lazy("students:student_create")
        return context


class StudentDetailView(mixins.HybridDetailView):
    model = Student
    permissions = ("management", "teacher", "branch", "accountant")

    def get_queryset(self):
        base_queryset = self.model.objects.filter(is_active=True)
        user_type = self.request.user.usertype
        if user_type == "branch":
            base_queryset = base_queryset.filter(batch__branch__user=self.request.user)
        return base_queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Student"
        return context


class StudentCreateView(mixins.HybridCreateView):
    model = Student
    permissions = ("management", "teacher", "branch", "accountant")

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        if "pk" in self.kwargs:
            user = get_object_or_404(User, pk=self.kwargs["pk"])
            form.fields["user"].initial = user
            form.fields["user"].disabled = True
            form.fields["first_name"].initial = user.first_name
            form.fields["admission_number"].initial = user.username
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Student"
        return context


class StudentUpdateView(mixins.HybridUpdateView):
    model = Student
    exclude = ("creator", "is_active")
    permissions = ("management", "teacher", "branch", "accountant")

    def get_queryset(self):
        base_queryset = self.model.objects.filter(is_active=True)
        user_type = self.request.user.usertype
        if user_type == "branch":
            base_queryset = base_queryset.filter(batch__branch__user=self.request.user)
        return base_queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Update Student"
        return context


class StudentDeleteView(mixins.HybridDeleteView):
    model = Student
    permissions = ("management",)


class StudentFeeStatementListView(mixins.HybridListView):
    model = StudentFeeStatement
    table_class = tables.StudentFeeStatementTable
    filterset_fields = {
        "student": ["exact"],
        "academic_year": ["exact"],
        "account": ["exact"],
        "date": ["lte"],
    }
    permissions = ("management", "accountant", "branch", "student")

    def get_queryset(self):
        base_queryset = self.model.objects.filter(is_active=True)
        if self.request.user.usertype == "branch":
            base_queryset = base_queryset.filter(account__user=self.request.user)
        elif self.request.user.usertype == "student":
            base_queryset = base_queryset.filter(student__user=self.request.user)
        return base_queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Student Receipts"
        if self.request.user.usertype == "student":
            context["title"] = "Payments"
        context["is_studentfeestatements"] = True
        context["can_add"] = mixins.check_access(self.request, ("accountant", "management"))
        context["new_link"] = reverse_lazy("students:studentfeestatement_create")
        return context


class StudentFeeStatementDetailView(mixins.HybridDetailView):
    model = StudentFeeStatement
    permissions = ("management", "accountant", "branch", "student")

    def get_queryset(self):
        base_queryset = self.model.objects.filter(is_active=True)
        if self.request.user.usertype == "branch":
            base_queryset = base_queryset.filter(student__batch__branch__user=self.request.user)
        elif self.request.user.usertype == "student":
            base_queryset = base_queryset.filter(student__user=self.request.user)
        return base_queryset


class StudentFeeStatementCreateView(mixins.HybridCreateView):
    model = StudentFeeStatement
    exclude = ("is_active", "creator")
    permissions = ("accountant", "management")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Student Receipt"
        return context


class StudentFeeStatementUpdateView(mixins.HybridUpdateView):
    model = StudentFeeStatement
    permissions = ("accountant", "management")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Student Receipt"
        return context


class StudentFeeStatementDeleteView(mixins.HybridDeleteView):
    model = StudentFeeStatement
    permissions = ("accountant", "management")


class AcademicYearStudentFeeListView(mixins.HybridListView):
    model = AcademicYearStudentFee
    table_class = tables.AcademicYearStudentFeeTable
    filterset_fields = {
        "student": ["exact"],
        "student__admission_number": ["icontains"],
        "student__division__standard": ["exact"],
        "student__division__name": ["icontains"],
        "academic_year": ["exact"],
    }
    permissions = ("management", "accountant", "student")

    def get_queryset(self):
        base_queryset = self.model.objects.filter(is_active=True)
        if self.request.user.usertype == "student":
            base_queryset = base_queryset.filter(student__user=self.request.user)
        return base_queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Academic Year Student Fees"
        context["is_academic_year_student_fees"] = True
        context["can_add"] = mixins.check_access(self.request, ("accountant", "management"))
        context["new_link"] = reverse_lazy("students:academic_year_student_fee_create")
        return context


class AcademicYearStudentFeeDetailView(mixins.HybridDetailView):
    model = AcademicYearStudentFee
    permissions = ("management", "accountant", "student")
    template_name = "students/academicyearstudentfee_detail.html"

    def get_queryset(self):
        base_queryset = self.model.objects.filter(is_active=True)
        if self.request.user.usertype == "student":
            base_queryset = base_queryset.filter(student__user=self.request.user)
        return base_queryset


class AcademicYearStudentFeeCreateView(mixins.HybridCreateView):
    model = AcademicYearStudentFee
    permissions = ("accountant", "management")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Academic Year Student Fee"
        return context


class AcademicYearStudentFeeUpdateView(mixins.HybridUpdateView):
    model = AcademicYearStudentFee
    permissions = ("accountant", "management")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Academic Year Student Fee"
        return context


class AcademicYearStudentFeeDeleteView(mixins.HybridDeleteView):
    model = AcademicYearStudentFee
    permissions = ("accountant", "management")


class StandardListView(mixins.HybridListView):
    model = Standard
    table_class = tables.StandardTable
    filterset_fields = {"name": ["icontains"]}
    permissions = ("management",)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Standards"
        context["is_standards"] = True
        context["can_add"] = mixins.check_access(self.request, ("management",))
        context["new_link"] = reverse_lazy("students:standard_create")
        return context


class StandardDetailView(mixins.HybridDetailView):
    model = Standard
    permissions = ("management",)


class StandardCreateView(mixins.HybridCreateView):
    model = Standard
    permissions = ("management",)


class StandardUpdateView(mixins.HybridUpdateView):
    model = Standard
    permissions = ("management",)


class StandardDeleteView(mixins.HybridDeleteView):
    model = Standard
    permissions = ("management",)


class DivisionListView(mixins.HybridListView):
    model = Division
    table_class = tables.DivisionTable
    filterset_fields = {
        "standard": ["exact"],
        "name": ["icontains"],
        "tutor": ["exact"],
    }
    permissions = ("management",)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Divisions"
        context["is_divisions"] = True
        context["can_add"] = mixins.check_access(self.request, ("management",))
        context["new_link"] = reverse_lazy("students:division_create")
        return context


class DivisionDetailView(mixins.HybridDetailView):
    model = Division
    permissions = ("management",)


class DivisionCreateView(mixins.HybridCreateView):
    model = Division
    permissions = ("management",)


class DivisionUpdateView(mixins.HybridUpdateView):
    model = Division
    permissions = ("management",)


class DivisionDeleteView(mixins.HybridDeleteView):
    model = Division
    permissions = ("management",)
