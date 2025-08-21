from datetime import date, timedelta

from accounting.models import Contra, Expense, ExpensePayment, Income
from core import mixins
from django.shortcuts import render
from employees.models import EmployeePayment, EmployeePayroll
from students.models import AcademicYearStudentFee, StudentFeeStatement

from . import functions, tables
from .forms import CashFlowForm, EmployeeReportForm, PNLReportForm


class StudentMasterDataView(mixins.HybridListView):
    model = AcademicYearStudentFee
    permissions = ("management", "accountant")
    template_name = "reports/student_master_data.html"
    table_class = tables.StudentMasterTable
    filterset_fields = {
        "academic_year": ["exact"],
        "student__first_name": ["icontains"],
        "student__admission_number": ["icontains"],
        "student__division__standard": ["exact"],
    }
    table_pagination = {"per_page": 30}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Student Master Data"
        context["is_student_master_data"] = True
        return context


class CashFlowView(mixins.HybridView):
    template_name = "reports/cash_flow.html"
    permissions = ("management", "accountant")

    def get(self, request, **kwargs):
        form = CashFlowForm(request.GET or None)
        employee_payment_qs = None
        employee_payment = 0
        other_expense_qs = None
        other_expense = 0
        student_receipt_income_qs = None
        student_receipt_income = 0
        contra_expense_qs = None
        contra_expense = 0
        contra_income_qs = None
        contra_income = 0
        other_income_qs = 0
        other_income = 0
        opening_balance = 0
        closing_balance = 0
        current_dr = 0
        current_cr = 0
        account = None
        if form.is_valid():
            startdate = form.cleaned_data.get("start_date")
            enddate = form.cleaned_data.get("end_date")
            account = form.cleaned_data.get("account")
            # current dr
            employee_payment_qs = EmployeePayment.objects.filter(date__range=(startdate, enddate), account=account, is_active=True)
            employee_payment = sum([item.amount for item in employee_payment_qs])
            other_expense_qs = ExpensePayment.objects.filter(date__range=(startdate, enddate), debit_account=account, is_active=True)
            other_expense = sum([item.amount for item in other_expense_qs])
            contra_expense_qs = Contra.objects.filter(date__range=(startdate, enddate), from_account=account, is_active=True)
            contra_expense = sum(item.amount for item in contra_expense_qs)
            current_dr = employee_payment + other_expense + contra_expense
            # opening dr
            opening_employee_payment_qs = EmployeePayment.objects.filter(date__lt=startdate, account=account, is_active=True)
            opening_employee_payment = sum([item.amount for item in opening_employee_payment_qs])
            opening_other_expense_qs = ExpensePayment.objects.filter(date__lt=startdate, debit_account=account, is_active=True)
            opening_other_expense = sum([item.amount for item in opening_other_expense_qs])
            opening_contra_expense_qs = Contra.objects.filter(date__lt=startdate, from_account=account, is_active=True)
            opening_contra_expense = sum(item.amount for item in opening_contra_expense_qs)
            # current cr
            student_receipt_income_qs = StudentFeeStatement.objects.filter(date__range=(startdate, enddate), account=account, is_active=True)
            student_receipt_income = sum([item.amount for item in student_receipt_income_qs])
            other_income_qs = Income.objects.filter(date__range=(startdate, enddate), credit_account=account, is_active=True)
            other_income = sum([item.amount for item in other_income_qs])
            contra_income_qs = Contra.objects.filter(date__range=(startdate, enddate), to_account=account, is_active=True)
            contra_income = sum(item.amount for item in contra_income_qs)
            current_cr = student_receipt_income + other_income + contra_income
            # opening cr
            opening_student_receipt_income_qs = StudentFeeStatement.objects.filter(date__lt=startdate, account=account, is_active=True)
            opening_student_receipt_income = sum([item.amount for item in opening_student_receipt_income_qs])
            opening_other_income_qs = Income.objects.filter(date__lt=startdate, credit_account=account, is_active=True)
            opening_other_income = sum([item.amount for item in opening_other_income_qs])
            opening_contra_income_qs = Contra.objects.filter(date__lt=startdate, to_account=account, is_active=True)
            opening_contra_income = sum(item.amount for item in opening_contra_income_qs)

            opening_balance = (
                opening_student_receipt_income + opening_other_income + opening_contra_income - opening_employee_payment - opening_other_expense - opening_contra_expense
            )
            closing_balance = opening_balance + student_receipt_income + other_income + contra_income - employee_payment - other_expense - contra_expense
        context = {
            "form": form,
            "is_cash_flow": True,
            "employee_payment_qs": employee_payment_qs,
            "employee_payment": employee_payment,
            "other_expense_qs": other_expense_qs,
            "other_expense": other_expense,
            "contra_income_qs": contra_income_qs,
            "contra_income": contra_income,
            "contra_expense_qs": contra_expense_qs,
            "contra_expense": contra_expense,
            "student_receipt_income_qs": student_receipt_income_qs,
            "student_receipt_income": student_receipt_income,
            "other_income_qs": other_income_qs,
            "other_income": other_income,
            "opening_balance": opening_balance,
            "closing_balance": closing_balance,
            "current_dr": current_dr,
            "current_cr": current_cr,
            "title": "Cash Flow",
            "account": account,
        }
        return render(request, self.template_name, context)


class EmployeeReportView(mixins.HybridView):
    template_name = "reports/employee_report.html"
    permissions = ("management", "accountant")

    def get(self, request, **kwargs):
        form = EmployeeReportForm(request.GET or None)
        opening_balance = 0
        closing_balance = 0
        total_payroll = 0
        total_payment = 0
        payrolls = None
        payments = None
        employee = None
        total_payroll = 0
        total_payment = 0
        if form.is_valid():
            startdate = form.cleaned_data.get("start_date")
            enddate = form.cleaned_data.get("end_date")
            employee = form.cleaned_data.get("employee")
            # current
            payrolls = EmployeePayroll.objects.filter(
                month__range=[startdate.month, enddate.month],
                year__range=[startdate.year, enddate.year],
                employee=employee,
                is_active=True,
            )
            payments = EmployeePayment.objects.filter(date__range=(startdate, enddate), employee=employee, is_active=True)
            total_payroll = sum([item.amount for item in payrolls])
            total_payment = sum([item.amount for item in payments])

            # opening
            opening_payrolls = EmployeePayroll.objects.filter(
                month__lt=startdate.month,
                year__lte=startdate.year,
                employee=employee,
                is_active=True,
            )
            opening_payments = EmployeePayment.objects.filter(date__lt=startdate, employee=employee, is_active=True)
            total_opening_payroll = sum([item.amount for item in opening_payrolls])
            total_opening_payment = sum([item.amount for item in opening_payments])

            opening_balance = total_opening_payroll - total_opening_payment
            closing_balance = opening_balance + total_payroll - total_payment
        context = {
            "form": form,
            "is_employee_report": True,
            "title": "Employee Report",
            "opening_balance": opening_balance,
            "closing_balance": closing_balance,
            "payrolls": payrolls,
            "payments": payments,
            "total_payroll": total_payroll,
            "total_payment": total_payment,
            "employee": employee,
        }
        return render(request, self.template_name, context)


class PNLView(mixins.HybridView):
    permissions = ("management", "accountant")
    template_name = "reports/pnl.html"

    def get(self, request, **kwargs):
        total_cr = 0
        total_dr = 0
        other_income_qs = None
        other_expense_qs = None
        payroll_qs = None
        net_profit = 0
        school_fee_due = 0
        form = PNLReportForm(request.GET or None)
        if form.is_valid():
            startdate = form.cleaned_data.get("start_date")
            enddate = form.cleaned_data.get("end_date")
            academic_years = functions.get_academic_years(startdate, enddate)
            academic_year_student_fee_qs = AcademicYearStudentFee.objects.filter(is_active=True, academic_year__in=academic_years)
            current_date = startdate
            unique_months_list = []
            while current_date <= enddate:
                unique_months_list.append((current_date.year, current_date.strftime("%B")))
                current_date = date(current_date.year, current_date.month, 1) + timedelta(days=32)

            for year, month in unique_months_list:
                for student_fee in academic_year_student_fee_qs:
                    due_fee = functions.get_due_fee(student_fee, month)
                    school_fee_due += due_fee
            other_income_qs = Income.objects.filter(
                credit_account__user__usertype="accountant",
                date__range=(startdate, enddate),
                is_active=True,
            )
            total_other_income = sum([item.amount for item in other_income_qs])
            total_cr = total_other_income + school_fee_due
            # DR
            payroll_qs = EmployeePayroll.objects.filter(
                month__range=(startdate.month, enddate.month),
                year__range=(startdate.year, enddate.year),
                is_active=True,
            )
            total_payroll = sum([item.amount for item in payroll_qs])
            other_expense_qs = Expense.objects.filter(date__range=(startdate, enddate), is_active=True)
            total_other_expense = sum([item.amount for item in other_expense_qs])
            total_dr = total_payroll + total_other_expense
            net_profit = total_cr - total_dr
        context = {
            "form": form,
            "is_pnl_report": True,
            "title": "Profit And Loss Statement (P&L)",
            "school_fee_due": school_fee_due,
            "other_income_qs": other_income_qs,
            "payroll_qs": payroll_qs,
            "other_expense_qs": other_expense_qs,
            "total_cr": total_cr,
            "total_dr": total_dr,
            "net_profit": net_profit,
        }
        return render(request, self.template_name, context)
