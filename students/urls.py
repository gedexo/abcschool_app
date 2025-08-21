from django.urls import path

from . import views

app_name = "students"

urlpatterns = [
    #ajax 
    path("get-divisions/", views.get_divisions, name="get_divisions"),
    path("", views.StudentListView.as_view(), name="student_list"),
    path("student/<str:pk>/", views.StudentDetailView.as_view(), name="student_detail"),
    path("new/student/", views.StudentCreateView.as_view(), name="student_create"),
    path(
        "new/student/<str:pk>/",
        views.StudentCreateView.as_view(),
        name="student_create",
    ),
    path(
        "student/<str:pk>/update/",
        views.StudentUpdateView.as_view(),
        name="student_update",
    ),
    path(
        "student/<str:pk>/delete/",
        views.StudentDeleteView.as_view(),
        name="student_delete",
    ),
    path(
        "studentfeestatements/",
        views.StudentFeeStatementListView.as_view(),
        name="studentfeestatement_list",
    ),
    path(
        "studentfeestatement/<str:pk>/",
        views.StudentFeeStatementDetailView.as_view(),
        name="studentfeestatement_detail",
    ),
    path(
        "new/studentfeestatement/",
        views.StudentFeeStatementCreateView.as_view(),
        name="studentfeestatement_create",
    ),
    path(
        "studentfeestatement/<str:pk>/update/",
        views.StudentFeeStatementUpdateView.as_view(),
        name="studentfeestatement_update",
    ),
    path(
        "studentfeestatement/<str:pk>/delete/",
        views.StudentFeeStatementDeleteView.as_view(),
        name="studentfeestatement_delete",
    ),
    path(
        "academic_year_student_fees/",
        views.AcademicYearStudentFeeListView.as_view(),
        name="academic_year_student_fee_list",
    ),
    path(
        "academic_year_student_fee/<str:pk>/",
        views.AcademicYearStudentFeeDetailView.as_view(),
        name="academic_year_student_fee_detail",
    ),
    path(
        "new/academic_year_student_fee/",
        views.AcademicYearStudentFeeCreateView.as_view(),
        name="academic_year_student_fee_create",
    ),
    path(
        "academic_year_student_fee/<str:pk>/update/",
        views.AcademicYearStudentFeeUpdateView.as_view(),
        name="academic_year_student_fee_update",
    ),
    path(
        "academic_year_student_fee/<str:pk>/delete/",
        views.AcademicYearStudentFeeDeleteView.as_view(),
        name="academic_year_student_fee_delete",
    ),
    path("standards/", views.StandardListView.as_view(), name="standard_list"),
    path("standard/<str:pk>/", views.StandardDetailView.as_view(), name="standard_detail"),
    path("new/standard/", views.StandardCreateView.as_view(), name="standard_create"),
    path(
        "standard/<str:pk>/update/",
        views.StandardUpdateView.as_view(),
        name="standard_update",
    ),
    path(
        "standard/<str:pk>/delete/",
        views.StandardDeleteView.as_view(),
        name="standard_delete",
    ),
    path("divisions/", views.DivisionListView.as_view(), name="division_list"),
    path("division/<str:pk>/", views.DivisionDetailView.as_view(), name="division_detail"),
    path("new/Division/", views.DivisionCreateView.as_view(), name="division_create"),
    path(
        "division/<str:pk>/update/",
        views.DivisionUpdateView.as_view(),
        name="division_update",
    ),
    path(
        "division/<str:pk>/delete/",
        views.DivisionDeleteView.as_view(),
        name="division_delete",
    ),
    path("transfer/<str:pk>/", views.StudentTransferUpdateView.as_view(), name="student_transfer_update")
]
