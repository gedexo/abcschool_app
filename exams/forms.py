from django import forms
from django.db import transaction
from students.models import Division, Student

from .models import Exam, StudentExam


class ExamForm(forms.ModelForm):
    division = forms.ModelChoiceField(
        queryset=Division.objects.filter(is_active=True),
        label="Select Class",
    )

    class Meta:
        model = Exam
        exclude = ("is_active",)

    @transaction.atomic
    def save(self, commit=True):
        exam = super().save(commit=False)

        # Save the exam for each student in the selected division
        selected_division = self.cleaned_data["division"]
        students_in_division = Student.objects.filter(division=selected_division)

        if commit:
            exam.save()

            # Save the exam for each student
            for student in students_in_division:
                student_exam = StudentExam(exam=exam, student=student)
                student_exam.save()

        return exam
