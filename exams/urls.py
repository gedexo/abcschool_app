from django.urls import path

from . import views

app_name = "exams"

urlpatterns = [
    path("series/", views.SeriesListView.as_view(), name="series_list"),
    path("series/<str:pk>/", views.SeriesDetailView.as_view(), name="series_detail"),
    path("new/series/", views.SeriesCreateView.as_view(), name="series_create"),
    path(
        "series/<str:pk>/update/",
        views.SeriesUpdateView.as_view(),
        name="series_update",
    ),
    path(
        "series/<str:pk>/delete/",
        views.SeriesDeleteView.as_view(),
        name="series_delete",
    ),
    path("exams/", views.ExamListView.as_view(), name="exam_list"),
    path("exam/<str:pk>/", views.ExamDetailView.as_view(), name="exam_detail"),
    path("new/exam/", views.ExamCreateView.as_view(), name="exam_create"),
    path("exam/<str:pk>/update/", views.ExamUpdateView.as_view(), name="exam_update"),
    path("exam/<str:pk>/delete/", views.ExamDeleteView.as_view(), name="exam_delete"),
    path("student_exams/", views.StudentExamListView.as_view(), name="student_exam_list"),
    path(
        "student_exam/<str:pk>/",
        views.StudentExamDetailView.as_view(),
        name="student_exam_detail",
    ),
    path(
        "new/student_exam/",
        views.StudentExamCreateView.as_view(),
        name="student_exam_create",
    ),
    path(
        "student_exam/<str:pk>/update/",
        views.StudentExamUpdateView.as_view(),
        name="student_exam_update",
    ),
    path(
        "student_exam/<str:pk>/delete/",
        views.StudentExamDeleteView.as_view(),
        name="student_exam_delete",
    ),
    path(
        "student_mark/<str:pk>/update/",
        views.student_mark_update,
        name="student_mark_update",
    ),
]
