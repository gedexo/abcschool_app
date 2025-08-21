from core.base import BaseModel
from django.db import models
from django.urls import reverse_lazy
from tinymce.models import HTMLField


class Course(BaseModel):
    teacher = models.ForeignKey(
        "employees.Employee",
        on_delete=models.CASCADE,
    )
    standard = models.ForeignKey("students.Standard", on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    description = HTMLField()
    youtube_video_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse_lazy("courses:course_detail", kwargs={"pk": self.pk})

    @staticmethod
    def get_list_url():
        return reverse_lazy("courses:course_list")

    def get_update_url(self):
        return reverse_lazy("courses:course_update", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse_lazy("courses:course_delete", kwargs={"pk": self.pk})
