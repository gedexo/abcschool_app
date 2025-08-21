from django import forms
from django.db import transaction
from students.models import Division, Student

from .models import StudentTask, Task


class TaskForm(forms.ModelForm):
    division = forms.ModelChoiceField(
        queryset=Division.objects.filter(is_active=True),
        label="Select Class",
    )

    class Meta:
        model = Task
        exclude = ("assigned_teacher", "is_active")

    @transaction.atomic
    def save(self, commit=True):
        task = super().save(commit=False)

        # Save the task for each student in the selected division
        selected_division = self.cleaned_data["division"]
        students_in_division = Student.objects.filter(division=selected_division)

        if commit:
            task.save()

            # Save the task for each student
            for student in students_in_division:
                student_task = StudentTask(task=task, student=student, status="assigned")
                student_task.save()

        return task
