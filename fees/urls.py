from django.urls import path

from . import views

app_name = "fees"

urlpatterns = [
    path(
        "additional_fee_studentes/",
        views.AdditionalFeeStudentListView.as_view(),
        name="additional_fee_student_list",
    ),
    path(
        "additional_fee_student/<str:pk>/",
        views.AdditionalFeeStudentDetailView.as_view(),
        name="additional_fee_student_detail",
    ),
    path(
        "new/additional_fee_student/",
        views.AdditionalFeeStudentCreateView.as_view(),
        name="additional_fee_student_create",
    ),
    path(
        "new/additional_fee_standard/",
        views.AdditionalFeeStandardCreateView.as_view(),
        name="additional_fee_standard_create",
    ),
    path(
        "new/additional_fee_students/",
        views.AdditionalFeeStudentsCreateView.as_view(),
        name="additional_fee_students_create",
    ),
    path(
        "additional_fee_student/<str:pk>/update/",
        views.AdditionalFeeStudentUpdateView.as_view(),
        name="additional_fee_student_update",
    ),
    path(
        "additional_fee_student/<str:pk>/delete/",
        views.AdditionalFeeStudentDeleteView.as_view(),
        name="additional_fee_student_delete",
    ),
]
