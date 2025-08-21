import uuid

from core.functions import generate_fields
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from employees.models import Employee
from students.models import Student


class User(AbstractUser):
    usertype = models.CharField(
        max_length=20,
        choices=(
            ("management", "Management"),
            ("student", "Student"),
            ("teacher", "Teacher"),
            ("accountant", "Accountant"),
        ),
        default="student",
    )
    enc_key = models.UUIDField(default=uuid.uuid4, editable=False)

    class Meta:
        ordering = ["username", "usertype"]

    def get_fields(self):
        return generate_fields(self)

    def get_absolute_url(self):
        return reverse_lazy("accounts:user_detail", kwargs={"pk": self.pk})

    @staticmethod
    def get_list_url():
        return reverse_lazy("accounts:user_list")

    def get_update_url(self):
        return reverse_lazy("accounts:user_update", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse_lazy("accounts:user_delete", kwargs={"pk": self.pk})

    def __str__(self):
        if self.usertype == "student":
            # Include student username in the last for student usertype
            return f"{self.first_name} ({self.username})"
        elif self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        elif self.first_name:
            return str(self.first_name)
        else:
            return str(self.username)

    def get_password(self):
        return str(self.enc_key)[::-1]

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save()
        return HttpResponseRedirect(self.get_list_url())

    @property
    def fullname(self):
        if self.usertype == "student":
            if Student.objects.filter(user=self).exists():
                return self.student.fullname
            else:
                return self.username
        elif Employee.objects.filter(user=self).exists():
            full_name_parts = [
                part
                for part in [
                    self.employee.first_name,
                    self.employee.middle_name,
                    self.employee.last_name,
                ]
                if part is not None
            ]
            return " ".join(full_name_parts)
        else:
            return self.username
