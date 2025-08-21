from django.urls import path

from . import views

app_name = "employees"

urlpatterns = [
    path("", views.EmployeeListView.as_view(), name="employee_list"),
    path("employee/<str:pk>/", views.EmployeeDetailView.as_view(), name="employee_detail"),
    path("new/employee/", views.EmployeeCreateView.as_view(), name="employee_create"),
    path(
        "new/employee/<str:pk>/",
        views.EmployeeCreateView.as_view(),
        name="employee_create",
    ),
    path(
        "employee/<str:pk>/update/",
        views.EmployeeUpdateView.as_view(),
        name="employee_update",
    ),
    path(
        "employee/<str:pk>/delete/",
        views.EmployeeDeleteView.as_view(),
        name="employee_delete",
    ),
    path("designations/", views.DesignationListView.as_view(), name="designation_list"),
    path(
        "designation/<str:pk>/",
        views.DesignationDetailView.as_view(),
        name="designation_detail",
    ),
    path(
        "new/designation/",
        views.DesignationCreateView.as_view(),
        name="designation_create",
    ),
    path(
        "designation/<str:pk>/update/",
        views.DesignationUpdateView.as_view(),
        name="designation_update",
    ),
    path(
        "designation/<str:pk>/delete/",
        views.DesignationDeleteView.as_view(),
        name="designation_delete",
    ),
    path("departments/", views.DepartmentListView.as_view(), name="department_list"),
    path(
        "department/<str:pk>/",
        views.DepartmentDetailView.as_view(),
        name="department_detail",
    ),
    path(
        "new/department/",
        views.DepartmentCreateView.as_view(),
        name="department_create",
    ),
    path(
        "department/<str:pk>/update/",
        views.DepartmentUpdateView.as_view(),
        name="department_update",
    ),
    path(
        "department/<str:pk>/delete/",
        views.DepartmentDeleteView.as_view(),
        name="department_delete",
    ),
    path(
        "employeepayrolls/",
        views.EmployeePayrollListView.as_view(),
        name="employeepayroll_list",
    ),
    path(
        "employeepayroll/<str:pk>/",
        views.EmployeePayrollDetailView.as_view(),
        name="employeepayroll_detail",
    ),
    path(
        "new/employeepayroll/",
        views.EmployeePayrollCreateView.as_view(),
        name="employeepayroll_create",
    ),
    path(
        "employeepayroll/<str:pk>/update/",
        views.EmployeePayrollUpdateView.as_view(),
        name="employeepayroll_update",
    ),
    path(
        "employeepayroll/<str:pk>/delete/",
        views.EmployeePayrollDeleteView.as_view(),
        name="employeepayroll_delete",
    ),
    path(
        "employeepayment/",
        views.EmployeePaymentListView.as_view(),
        name="employeepayment_list",
    ),
    path(
        "employeepayment/<str:pk>/",
        views.EmployeePaymentDetailView.as_view(),
        name="employeepayment_detail",
    ),
    path(
        "new/employeepayment/",
        views.EmployeePaymentCreateView.as_view(),
        name="employeepayment_create",
    ),
    path(
        "employeepayment/<str:pk>/update/",
        views.EmployeePaymentUpdateView.as_view(),
        name="employeepayment_update",
    ),
    path(
        "employeepayment/<str:pk>/delete/",
        views.EmployeePaymentDeleteView.as_view(),
        name="employeepayment_delete",
    ),
]
