from django.urls import path

from . import views

app_name = "reports"

urlpatterns = [
    path("cash_flow/", views.CashFlowView.as_view(), name="cash_flow"),
    path("employee_report/", views.EmployeeReportView.as_view(), name="employee_report"),
    path("pnl_report/", views.PNLView.as_view(), name="pnl_report"),
    path(
        "student_master_data/",
        views.StudentMasterDataView.as_view(),
        name="student_master_data",
    ),
]
