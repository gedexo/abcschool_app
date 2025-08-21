from django import forms
from django.db import transaction
from students.models import Standard, Student

from .models import AdditionalFeeStudent


class AdditionalFeeStandardForm(forms.ModelForm):
    standard = forms.ModelChoiceField(queryset=Standard.objects.filter(is_active=True))

    class Meta:
        model = AdditionalFeeStudent
        fields = (
            "academic_year",
            "fee",
            "fee_name",
            "standard",
            "amount",
            "due_date",
            "remarks",
        )

    @transaction.atomic
    def save(self, commit=True):
        additional_fee = super().save(commit=False)
        selected_standard = self.cleaned_data["standard"]
        academic_year = self.cleaned_data["academic_year"]
        fee = self.cleaned_data["fee"]
        amount = self.cleaned_data["amount"]
        due_date = self.cleaned_data["due_date"]
        remarks = self.cleaned_data["remarks"]
        students_in_standard = Student.objects.filter(division__standard=selected_standard)

        if commit:
            for student in students_in_standard:
                student_additional_fee = AdditionalFeeStudent(
                    academic_year=academic_year,
                    fee=fee,
                    amount=amount,
                    due_date=due_date,
                    remarks=remarks,
                    student=student,
                )
                student_additional_fee.save()

        return additional_fee


class AdditionalFeeStudentsForm(forms.ModelForm):
    students = forms.ModelMultipleChoiceField(queryset=Student.objects.filter(is_active=True))

    class Meta:
        model = AdditionalFeeStudent
        fields = (
            "academic_year",
            "fee",
            "fee_name",
            "amount",
            "due_date",
            "students",
            "remarks",
        )

    @transaction.atomic
    def save(self, commit=True):
        additional_fee = super().save(commit=False)
        academic_year = self.cleaned_data["academic_year"]
        fee = self.cleaned_data["fee"]
        amount = self.cleaned_data["amount"]
        due_date = self.cleaned_data["due_date"]
        remarks = self.cleaned_data["remarks"]

        if commit:
            selected_students = self.cleaned_data["students"]
            for student in selected_students:
                student_additional_fee = AdditionalFeeStudent(
                    academic_year=academic_year,
                    fee=fee,
                    amount=amount,
                    due_date=due_date,
                    remarks=remarks,
                    student=student,
                )
                student_additional_fee.save()
        return additional_fee
