from django.db import models
from django.urls import reverse_lazy

from .base import BaseModel


class Suggestion(BaseModel):
    suggested_by = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    suggestion = models.TextField()

    def __str__(self):
        return f"{self.suggested_by} Suggestion"

    def get_absolute_url(self):
        return reverse_lazy("core:suggestion_detail", kwargs={"pk": self.pk})

    @staticmethod
    def get_list_url():
        return reverse_lazy("core:suggestion_list")

    def get_update_url(self):
        return reverse_lazy("core:suggestion_update", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse_lazy("core:suggestion_delete", kwargs={"pk": self.pk})
