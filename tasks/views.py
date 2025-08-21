from core import mixins
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from tasks.forms import TaskForm

from . import tables
from .models import StudentTask, Task


class TaskListView(mixins.HybridListView):
    model = Task
    table_class = tables.TaskTable
    filterset_fields = {
        "title": ["icontains"],
        "due_date": ["lte"],
        "assigned_teacher": ["exact"],
    }
    permissions = ("management", "teacher")

    def get_queryset(self):
        base_qs = super().get_queryset()
        if self.request.user.usertype == "teacher":
            base_qs = base_qs.filter(assigned_teacher=self.request.user.employee)
        return base_qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["can_add"] = mixins.check_access(self.request, ("management", "teacher"))
        context["new_link"] = reverse_lazy("tasks:task_create")
        return context


class TaskDetailView(mixins.HybridDetailView):
    model = Task
    permissions = ("management", "teacher")

    def get_queryset(self):
        base_qs = super().get_queryset()
        if self.request.user.usertype == "teacher":
            base_qs = base_qs.filter(assigned_teacher=self.request.user.employee)
        return base_qs


class TaskCreateView(mixins.CustomLoginRequiredMixin, mixins.CreateView):
    model = Task
    form_class = TaskForm
    template_name = "app/common/object_form.html"
    permissions = ("management", "teacher")

    def form_valid(self, form):
        form.instance.assigned_teacher = self.request.user.employee
        return super().form_valid(form)


class TaskUpdateView(mixins.HybridUpdateView):
    model = Task
    permissions = ("management", "teacher")

    def get_queryset(self):
        base_qs = super().get_queryset()
        if self.request.user.usertype == "teacher":
            base_qs = base_qs.filter(assigned_teacher=self.request.user.employee)
        return base_qs


class TaskDeleteView(mixins.HybridDeleteView):
    model = Task
    permissions = ("management", "teacher")

    def get_queryset(self):
        base_qs = super().get_queryset()
        if self.request.user.usertype == "teacher":
            base_qs = base_qs.filter(assigned_teacher=self.request.user.employee)
        return base_qs


class StudentTaskListView(mixins.HybridListView):
    model = StudentTask
    table_class = tables.StudentTaskTable
    filterset_fields = {
        "task__title": ["icontains"],
        "task__due_date": ["lte"],
        "status": ["exact"],
        "student": ["exact"],
    }
    permissions = ("management", "teacher", "student")
    template_name = "tasks/studenttask_filter.html.html"

    def get_queryset(self):
        base_qs = super().get_queryset()
        usertype = self.request.user.usertype
        if usertype == "teacher":
            base_qs = base_qs.filter(task__assigned_teacher=self.request.user.employee)
        elif usertype == "student":
            base_qs = base_qs.filter(student=self.request.user.student)
        return base_qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_student_tasks"] = True
        context["can_add"] = mixins.check_access(self.request, ("management", "teacher"))
        context["new_link"] = reverse_lazy("tasks:student_task_create")
        context["task_assigned"] = self.get_queryset().filter(status="assigned").count()
        context["task_in_review"] = self.get_queryset().filter(status="in_review").count()
        context["task_completed"] = self.get_queryset().filter(status="completed").count()
        context["task_rework"] = self.get_queryset().filter(status="rework").count()
        context["title"] = "Student Tasks"
        return context


class StudentTaskDetailView(mixins.HybridDetailView):
    model = StudentTask
    permissions = ("management", "teacher")

    def get_queryset(self):
        base_qs = super().get_queryset()
        usertype = self.request.user.usertype
        if usertype == "teacher":
            base_qs = base_qs.filter(task__assigned_teacher=self.request.user.employee)
        elif usertype == "student":
            base_qs = base_qs.filter(student=self.request.user.student)
        return base_qs


class StudentTaskCreateView(mixins.HybridCreateView):
    model = StudentTask
    exclude = ("is_active", "status")
    permissions = ("management", "teacher")


class StudentTaskUpdateView(mixins.HybridUpdateView):
    model = StudentTask
    exclude = ("is_active", "status")
    permissions = ("management", "teacher")

    def get_queryset(self):
        base_qs = super().get_queryset()
        usertype = self.request.user.usertype
        if usertype == "teacher":
            base_qs = base_qs.filter(task__assigned_teacher=self.request.user.employee)
        return base_qs


class StudentTaskDeleteView(mixins.HybridDeleteView):
    model = StudentTask
    permissions = ("management", "teacher")

    def get_queryset(self):
        base_qs = super().get_queryset()
        usertype = self.request.user.usertype
        if usertype == "teacher":
            base_qs = base_qs.filter(task__assigned_teacher=self.request.user.employee)
        return base_qs


def task_status_update(request, pk):
    crt_status = request.POST.get("status")
    task = get_object_or_404(StudentTask, pk=pk)
    task.status = crt_status
    task.save()
    return JsonResponse({"status": "success"})
