from django import forms
from students.models import Student,AcademicYearStudentFee


class StudentTransferForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ("standard", "division")


class TransferFeeForm(forms.ModelForm):
    class Meta:
        model = AcademicYearStudentFee
        fields = ("school_fee", "donation_fee", "pta_fee")