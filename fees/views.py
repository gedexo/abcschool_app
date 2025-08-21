from core import mixins
from django.urls import reverse_lazy
from fees.forms import AdditionalFeeStandardForm, AdditionalFeeStudentsForm

from . import tables
from .models import AdditionalFeeStudent


class AdditionalFeeStudentListView(mixins.HybridListView):
    model = AdditionalFeeStudent
    table_class = tables.AdditionalFeeStudentTable
    template_name = "fee/additional_fee_filter.html"
    filterset_fields = {
        "fee": ["exact"],
        "student__admission_number": ["icontains"],
        "student__first_name": ["icontains"],
        "academic_year": ["exact"],
        "due_date": ["lte"],
    }
    permissions = ("management", "accountant", "branch", "student")

    def get_queryset(self):
        if self.request.user.usertype == "student":
            return super().get_queryset().filter(student__user=self.request.user)
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Additional Fees"
        context["is_additional_fee_students"] = True
        context["can_add"] = mixins.check_access(self.request, ("accountant",))
        context["for_student"] = reverse_lazy("fees:additional_fee_student_create")
        context["for_standard"] = reverse_lazy("fees:additional_fee_standard_create")
        context["for_students"] = reverse_lazy("fees:additional_fee_students_create")
        return context


class AdditionalFeeStudentDetailView(mixins.HybridDetailView):
    model = AdditionalFeeStudent
    permissions = ("management", "accountant", "branch", "student")


class AdditionalFeeStudentCreateView(mixins.HybridCreateView):
    model = AdditionalFeeStudent
    exclude = ("creator", "is_active")
    permissions = ("accountant",)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Additional Fees"
        context["form_class"] = "form-horizontal-additional-fee"
        return context


class AdditionalFeeStandardCreateView(mixins.CustomLoginRequiredMixin, mixins.CreateView):
    model = AdditionalFeeStudent
    form_class = AdditionalFeeStandardForm
    permissions = ("accountant",)
    template_name = "app/common/object_form.html"

    def get_success_url(self):
        return reverse_lazy("fees:additional_fee_student_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Additional fees are applicable to students in the standard program"
        context["form_class"] = "form-horizontal-additional-fee"
        return context


class AdditionalFeeStudentsCreateView(mixins.CustomLoginRequiredMixin, mixins.CreateView):
    model = AdditionalFeeStudent
    form_class = AdditionalFeeStudentsForm
    permissions = ("accountant",)
    template_name = "app/common/object_form.html"

    def get_success_url(self):
        return reverse_lazy("fees:additional_fee_student_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Additional fees are applicable to selected students"
        context["form_class"] = "form-horizontal-additional-fee"
        return context


class AdditionalFeeStudentUpdateView(mixins.HybridUpdateView):
    model = AdditionalFeeStudent
    permissions = ("accountant",)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Additional Fees"
        context["form_class"] = "form-horizontal-additional-fee"
        return context


class AdditionalFeeStudentDeleteView(mixins.HybridDeleteView):
    model = AdditionalFeeStudent
    permissions = ("accountant",)
