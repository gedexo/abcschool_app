from django.urls import path

from . import views

app_name = "tasks"

urlpatterns = [
    path("tasks/", views.TaskListView.as_view(), name="task_list"),
    path("task/<str:pk>/", views.TaskDetailView.as_view(), name="task_detail"),
    path("new/task/", views.TaskCreateView.as_view(), name="task_create"),
    path("task/<str:pk>/update/", views.TaskUpdateView.as_view(), name="task_update"),
    path("task/<str:pk>/delete/", views.TaskDeleteView.as_view(), name="task_delete"),
    path("student_tasks/", views.StudentTaskListView.as_view(), name="student_task_list"),
    path(
        "student_task/<str:pk>/",
        views.StudentTaskDetailView.as_view(),
        name="student_task_detail",
    ),
    path(
        "new/student_task/",
        views.StudentTaskCreateView.as_view(),
        name="student_task_create",
    ),
    path(
        "student_task/<str:pk>/update/",
        views.StudentTaskUpdateView.as_view(),
        name="student_task_update",
    ),
    path(
        "student_task/<str:pk>/delete/",
        views.StudentTaskDeleteView.as_view(),
        name="student_task_delete",
    ),
    path(
        "task/<str:pk>/update_status/",
        views.task_status_update,
        name="task_status_update",
    ),
]
