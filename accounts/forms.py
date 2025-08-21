from django import forms
from django.forms import widgets
from employees.models import Employee
from students.models import Student


class EmployeeImageForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ("photo",)
        widgets = {"photo": widgets.FileInput(attrs={"class": "form-control-file d-none"})}


class StudentImageForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ("photo",)
        widgets = {"photo": widgets.FileInput(attrs={"class": "form-control-file d-none"})}
