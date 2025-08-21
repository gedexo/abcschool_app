from django.urls import path

from . import views

app_name = "hrms"

urlpatterns = [
    path(
        "leave_request/",
        views.LeaveRequestListView.as_view(),
        name="leave_request_list",
    ),
    path(
        "leave_request/<str:pk>/",
        views.LeaveRequestDetailView.as_view(),
        name="leave_request_detail",
    ),
    path(
        "new/leave_request/",
        views.LeaveRequestCreateView.as_view(),
        name="leave_request_create",
    ),
    path(
        "leave_request/<str:pk>/update/",
        views.LeaveRequestUpdateView.as_view(),
        name="leave_request_update",
    ),
    path(
        "leave_request/<str:pk>/delete/",
        views.LeaveRequestDeleteView.as_view(),
        name="leave_request_delete",
    ),
    path(
        "leave_request/<str:pk>/update_status/",
        views.leave_request_status_update,
        name="leave_request_status_update",
    ),
    path(
        "attendence/<str:pk>/update_status/",
        views.attendence_status_update,
        name="attendence_status_update",
    ),
    path("attendance/", views.AttendanceListView.as_view(), name="attendance_list"),
    path(
        "attendance/<str:pk>/",
        views.AttendanceDetailView.as_view(),
        name="attendance_detail",
    ),
    path(
        "new/attendance/",
        views.AttendanceCreateView.as_view(),
        name="attendance_create",
    ),
    path(
        "attendance/<str:pk>/delete/",
        views.AttendanceDeleteView.as_view(),
        name="attendance_delete",
    ),
]
