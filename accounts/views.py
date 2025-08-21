from accounts.forms import EmployeeImageForm, StudentImageForm
from core import mixins
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy

from . import tables
from .models import User


class UserListView(mixins.HybridListView):
    model = User
    table_class = tables.UserTable
    filterset_fields = {
        "username": ["icontains"],
        "first_name": ["icontains"],
        "usertype": ["exact"],
    }
    permissions = ("management", "teacher", "branch", "accountant")

    def get_queryset(self):
        base_queryset = super().get_queryset()
        user_type = self.request.user.usertype
        if user_type == "teacher":
            base_queryset = base_queryset.filter(usertype="student")
        if user_type == "branch":
            base_queryset = base_queryset.exclude(usertype="management")
        return base_queryset.exclude(is_superuser=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Users"
        context["is_users"] = True
        context["can_add"] = mixins.check_access(self.request, ("management", "teacher", "branch", "accountant"))
        context["new_link"] = reverse_lazy("accounts:user_create")
        return context


class UserDetailView(mixins.HybridDetailView):
    model = User
    permissions = ("management", "teacher", "branch", "accountant")


class UserCreateView(mixins.HybridCreateView):
    model = User
    exclude = (
        "is_active",
        "date_joined",
        "user_permissions",
        "groups",
        "last_login",
        "is_superuser",
        "is_staff",
        "last_name",
    )
    permissions = ("management", "teacher", "branch", "accountant")

    def get_success_url(self):
        if self.object.usertype in ("management", "teacher", "worker", "accountant"):
            url = reverse_lazy("employees:employee_create", kwargs={"pk": self.object.pk})
        else:
            url = reverse_lazy("students:student_create", kwargs={"pk": self.object.pk})
        return url

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.fields["first_name"].required = True
        if self.request.user.usertype == "teacher":
            form.fields["usertype"].choices = [
                ("student", "Student"),
            ]
        return form

    def form_valid(self, form):
        form.instance.set_password(form.cleaned_data["password"])
        return super().form_valid(form)


class UserUpdateView(mixins.HybridUpdateView):
    model = User
    exclude = (
        "is_active",
        "password",
        "date_joined",
        "user_permissions",
        "groups",
        "last_login",
        "is_superuser",
        "is_staff",
    )
    permissions = ("management", "teacher", "branch", "accountant")


class UserDeleteView(mixins.HybridDeleteView):
    model = User
    permissions = ("management", "teacher", "branch", "accountant")


class UserProfile(mixins.HybridView):
    template_name = "app/common/profile.html"
    permissions = ("management", "teacher", "branch", "accountant", "worker", "student")

    def get(self, request, **kwargs):
        if request.user.usertype in ("management", "teacher", "accountant", "worker"):
            user_object = self.request.user.employee
        else:
            user_object = self.request.user.student
        form = EmployeeImageForm(request.POST or None)
        if request.user.usertype == "student":
            form = StudentImageForm(request.POST or None)
        return render(request, self.template_name, {"object": user_object, "form": form})

    def post(self, request, *args, **kwargs):
        if request.user.usertype != "student":
            instance = request.user.employee
            form = EmployeeImageForm(request.POST, request.FILES, instance=instance)
        else:
            instance = request.user.student
            form = StudentImageForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            return JsonResponse({"status": True})
        else:
            return JsonResponse("Invalid method")
