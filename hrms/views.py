from core import mixins
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy

from . import tables
from .forms import AttendenceForm
from .models import Attendance, LeaveRequest


class LeaveRequestListView(mixins.HybridListView):
    model = LeaveRequest
    table_class = tables.LeaveRequestTable
    filterset_fields = ["employee", "status"]
    permissions = ("management", "teacher")
    template_name = "hrms/leaverequest_filter.html"

    def get_queryset(self):
        if self.request.user.usertype == "teacher":
            return super().get_queryset().filter(employee__user=self.request.user)
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_leave_requests"] = True
        context["can_add"] = mixins.check_access(self.request, ("teacher", "management"))
        context["can_edit"] = mixins.check_access(self.request, ("management"))
        context["new_link"] = reverse_lazy("hrms:leave_request_create")
        return context


class LeaveRequestDetailView(mixins.HybridDetailView):
    model = LeaveRequest
    permissions = ("management", "teacher")


class LeaveRequestCreateView(mixins.HybridCreateView):
    model = LeaveRequest
    exclude = ("employee", "is_active", "creator", "status", "remarks")
    permissions = ("management", "teacher")

    def form_valid(self, form):
        form.instance.employee = self.request.user.employee
        return super().form_valid(form)


class LeaveRequestUpdateView(mixins.HybridUpdateView):
    model = LeaveRequest
    exclude = ("employee", "is_active", "creator", "status", "remarks")
    permissions = ("management", "teacher")


class LeaveRequestDeleteView(mixins.HybridDeleteView):
    model = LeaveRequest
    permissions = ("management", "teacher")


def leave_request_status_update(request, pk):
    crt_status = request.POST.get("status")
    leave_request = get_object_or_404(LeaveRequest, pk=pk)
    leave_request.status = crt_status
    leave_request.save()
    return JsonResponse({"status": "success"})


class AttendanceListView(mixins.HybridListView):
    model = Attendance
    table_class = tables.AttendanceTable
    filterset_fields = {
        "student__division": ["exact"],
        "student__first_name": ["icontains"],
        "student__admission_number": ["icontains"],
        "date": ["exact"],
        "status": ["exact"],
    }
    permissions = ("management", "teacher", "student")
    template_name = "hrms/attendence_filter.html"

    def get_queryset(self):
        base_qs = super().get_queryset()
        usertype = self.request.user.usertype
        if usertype == "student":
            base_qs = base_qs.filter(student=self.request.user.student)
        elif usertype == "teacher":
            teacher = self.request.user.employee
            base_qs = base_qs.filter(attendance_recorder=teacher)
        return base_qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_attendance"] = True
        context["title"] = "Attendances"
        context["can_add"] = mixins.check_access(self.request, ("management", "teacher"))
        context["title"] = "Attendances"
        context["new_link"] = reverse_lazy("hrms:attendance_create")
        return context


class AttendanceDetailView(mixins.HybridDetailView):
    model = Attendance
    permissions = ("management", "teacher", "student")


class AttendanceCreateView(mixins.HybridView):
    permissions = ("management", "teacher", "student")
    template_name = "hrms/add_attendence.html"

    def get(self, request, **kwargs):
        form = AttendenceForm(request.GET or None)
        students = self.get_students_from_form(form)
        context = {"form": form, "students": students, "title": "Attendence"}
        return render(request, self.template_name, context)

    def post(self, request, **kwargs):
        form = AttendenceForm(request.GET or None)
        students = self.get_students_from_form(form)
        student_ids = request.POST.getlist("studentCheckbox")
        date = request.POST.get("date")

        for student in students:
            if str(student.pk) in student_ids:
                is_present = "present"
            else:
                is_present = "absent"

            attendance, created = Attendance.objects.get_or_create(
                student=student,
                date=date,
                attendance_recorder=request.user.employee
            )
            attendance.status = is_present
            attendance.save()

        return redirect("hrms:attendance_list")

    def get_students_from_form(self, form):
        students = None
        if form.is_valid():
            division = form.cleaned_data.get("division")
            students = division.students.filter(is_active=True)
        return students


class AttendanceDeleteView(mixins.HybridDeleteView):
    model = Attendance
    permissions = ("management", "teacher")


def attendence_status_update(request, pk):
    crt_status = request.POST.get("status")
    attendence = get_object_or_404(Attendance, pk=pk)
    attendence.status = crt_status
    attendence.save()
    return JsonResponse({"status": "success"})
