from django.urls import path

from . import views

app_name = "courses"

urlpatterns = [
    path("", views.CourseListView.as_view(), name="course_list"),
    path("course/<str:pk>/", views.CourseDetailView.as_view(), name="course_detail"),
    path("new/course/", views.CourseCreateView.as_view(), name="course_create"),
    path(
        "course/<str:pk>/update/",
        views.CourseUpdateView.as_view(),
        name="course_update",
    ),
    path(
        "course/<str:pk>/delete/",
        views.CourseDeleteView.as_view(),
        name="course_delete",
    ),
]
