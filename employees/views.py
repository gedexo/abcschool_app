from accounts.models import User
from core import mixins
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy

from . import tables
from .models import Department, Designation, Employee, EmployeePayment, EmployeePayroll


class DesignationListView(mixins.HybridListView):
    model = Designation
    table_class = tables.DesignationTable
    filterset_fields = {"name": ["icontains"]}
    permissions = ("management",)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Designations"
        context["is_designations"] = True
        context["can_add"] = mixins.check_access(self.request, ("management", "branch"))
        context["new_link"] = reverse_lazy("employees:designation_create")
        return context


class DesignationDetailView(mixins.HybridDetailView):
    model = Designation
    permissions = ("management",)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Designation"
        return context


class DesignationCreateView(mixins.HybridCreateView):
    model = Designation
    fields = ("name", "description")
    permissions = ("management",)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "New Designation"
        return context


class DesignationUpdateView(mixins.HybridUpdateView):
    model = Designation
    fields = (
        "name",
        "description",
    )
    permissions = ("management",)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Update Designation"
        return context


class DesignationDeleteView(mixins.HybridDeleteView):
    model = Designation
    permissions = ("management",)


class DesignationApproveView(mixins.HybridUpdateView):
    model = Designation
    fields = ("status",)
    permissions = ("management",)


class DesignationRejectView(mixins.HybridUpdateView):
    model = Designation
    fields = ("status",)
    permissions = ("management",)


class DepartmentListView(mixins.HybridListView):
    model = Department
    table_class = tables.DepartmentTable
    filterset_fields = {
        "name": ["icontains"],
        "department_lead": ["exact"],
    }
    permissions = ("management",)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Departments"
        context["is_departments"] = "Departments"
        context["can_add"] = mixins.check_access(self.request, ("management", "accounts", "hod", "marketing", "worker"))
        context["new_link"] = reverse_lazy("employees:department_create")
        return context


class DepartmentDetailView(mixins.HybridDetailView):
    model = Department
    permissions = ("management", "accounts", "hod", "marketing", "worker")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Department"
        return context


class DepartmentCreateView(mixins.HybridCreateView):
    model = Department
    fields = ("name", "description", "department_lead")
    permissions = ("management",)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "New Department"
        return context


class DepartmentUpdateView(mixins.HybridUpdateView):
    model = Department
    fields = (
        "name",
        "description",
        "department_lead",
    )
    permissions = ("management",)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Update Department"
        return context


class DepartmentDeleteView(mixins.HybridDeleteView):
    model = Department
    permissions = ("management",)


class EmployeeListView(mixins.HybridListView):
    model = Employee
    table_class = tables.EmployeeTable
    filterset_fields = {
        "user__usertype": ["exact"],
        "first_name": ["icontains"],
    }
    permissions = ("management", "branch", "accountant")

    def get_queryset(self):
        base_queryset = super(EmployeeListView, self).get_queryset()
        if self.request.user.usertype == "branch":
            base_queryset = base_queryset.exclude(user__usertype="management")
        return base_queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_employees"] = True
        context["can_add"] = mixins.check_access(self.request, ("management", "branch"))
        context["new_link"] = reverse_lazy("employees:employee_create")
        return context


class EmployeeDetailView(mixins.HybridDetailView):
    model = Employee
    permissions = ("management", "branch", "accountant")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Employee"
        return context


class EmployeeCreateView(mixins.HybridCreateView):
    model = Employee
    exclude = (
        "creator",
        "is_active",
    )
    permissions = ("management", "branch", "accountant")

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        if "pk" in self.kwargs:
            user = get_object_or_404(User, pk=self.kwargs["pk"])
            form.fields["user"].initial = user
            form.fields["user"].disabled = True
            form.fields["first_name"].initial = user.first_name
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "New Employee"
        return context


class EmployeeUpdateView(mixins.HybridUpdateView):
    model = Employee
    permissions = ("management", "branch", "accountant")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Update Employee"
        return context


class EmployeeDeleteView(mixins.HybridDeleteView):
    model = Employee
    permissions = ("management", "branch", "accountant")


class EmployeePayrollListView(mixins.HybridListView):
    model = EmployeePayroll
    table_class = tables.EmployeePayrollTable
    filterset_fields = ["employee", "month", "year"]
    permissions = ("management", "accountant", "teacher")

    def get_queryset(self):
        base_queryset = self.model.objects.filter(is_active=True)
        if self.request.user.usertype == "teacher":
            base_queryset = base_queryset.filter(employee__user=self.request.user)
        return base_queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Employee Payrolls"
        context["is_employeepayrolls"] = True
        context["can_add"] = mixins.check_access(self.request, ("accountant"))
        context["new_link"] = reverse_lazy("employees:employeepayroll_create")
        return context


class EmployeePayrollDetailView(mixins.HybridDetailView):
    model = EmployeePayroll
    permissions = ("management", "accountant", "teacher")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Employment Payroll"
        return context


class EmployeePayrollCreateView(mixins.HybridCreateView):
    model = EmployeePayroll
    exclude = ("creator", "is_active", "time_out", "status", "remarks")
    permissions = ("accountant",)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "New Employment Payroll"
        return context


class EmployeePayrollUpdateView(mixins.HybridUpdateView):
    model = EmployeePayroll
    permissions = ("accountant",)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Update EmployeePayroll"
        return context


class EmployeePayrollDeleteView(mixins.HybridDeleteView):
    model = EmployeePayroll
    permissions = ("accountant",)


class EmployeePaymentListView(mixins.HybridListView):
    model = EmployeePayment
    table_class = tables.EmployeePaymentTable
    filterset_fields = ("employee", "amount", "account", "date")
    permissions = ("management", "accountant", "teacher")

    def get_queryset(self):
        base_queryset = self.model.objects.filter(is_active=True)
        if self.request.user.usertype == "branch":
            base_queryset = base_queryset.filter(account__user=self.request.user)
        if self.request.user.usertype == "teacher":
            base_queryset = base_queryset.filter(employee__user=self.request.user)
        return base_queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Employee Payments"
        context["is_employeepayment"] = True
        context["can_add"] = mixins.check_access(self.request, ("accountant",))
        context["new_link"] = reverse_lazy("employees:employeepayment_create")
        return context


class EmployeePaymentDetailView(mixins.HybridDetailView):
    model = EmployeePayment
    permissions = ("management", "accountant", "teacher")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Employee Payments"
        return context


class EmployeePaymentCreateView(mixins.HybridCreateView):
    model = EmployeePayment
    exclude = ("is_active", "creator")
    permissions = ("accountant",)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Employee Payments"
        return context


class EmployeePaymentUpdateView(mixins.HybridUpdateView):
    model = EmployeePayment
    exclude = ("is_active", "creator")
    permissions = ("accountant",)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Employee Payments"
        return context


class EmployeePaymentDeleteView(mixins.HybridDeleteView):
    model = EmployeePayment
    permissions = ("accountant",)
