from django import forms
from django.utils import timezone
from students.models import Division


class AttendenceForm(forms.Form):
    date = forms.DateField()
    division = forms.ModelChoiceField(queryset=Division.objects.all())

    def clean_date(self):
        date = self.cleaned_data.get("date")
        if date and date > timezone.now().date():
            raise forms.ValidationError("Cannot select a future date.")
        return date
