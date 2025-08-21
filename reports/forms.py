from accounting.models import Account
from django import forms
from employees.models import Employee


class EmployeeReportForm(forms.Form):
    start_date = forms.DateField()
    end_date = forms.DateField()
    employee = forms.ModelChoiceField(queryset=Employee.objects.all())


class CashFlowForm(forms.Form):
    start_date = forms.DateField()
    end_date = forms.DateField()
    account = forms.ModelChoiceField(queryset=Account.objects.filter(is_active=True))


class BranchReportForm(forms.Form):
    pass


class PNLReportForm(forms.Form):
    start_date = forms.DateField()
    end_date = forms.DateField()
