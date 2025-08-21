from core import mixins
from django.urls import reverse_lazy

from . import tables
from .models import Course


class CourseListView(mixins.HybridListView):
    model = Course
    table_class = tables.CourseTable
    filterset_fields = {
        "title": ["icontains"],
        "teacher": ["exact"],
    }
    permissions = ("management", "teacher", "student")

    def get_queryset(self):
        usertype = self.request.user.usertype
        if usertype == "teacher":
            return super().get_queryset().filter(teacher=self.request.user.employee)
        elif usertype == "student":
            return super().get_queryset().filter(standard=self.request.user.student.standard)
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Courses"
        context["is_courses"] = True
        context["can_add"] = mixins.check_access(self.request, ("teacher", "management"))
        context["new_link"] = reverse_lazy("courses:course_create")
        return context


class CourseDetailView(mixins.HybridDetailView):
    model = Course
    permissions = ("management", "teacher", "student")


class CourseCreateView(mixins.HybridCreateView):
    model = Course
    exclude = ("is_active", "creator", "teacher")
    permissions = ("teacher", "management")

    def form_valid(self, form):
        form.instance.teacher = self.request.user.employee
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Course"
        return context


class CourseUpdateView(mixins.HybridUpdateView):
    model = Course
    exclude = ("is_active", "creator", "teacher")
    permissions = ("teacher", "management")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Course"
        return context


class CourseDeleteView(mixins.HybridDeleteView):
    model = Course
    permissions = ("management", "teacher", "student")
