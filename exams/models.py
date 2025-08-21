from core.base import BaseModel
from django.db import models
from django.urls import reverse_lazy


class Series(BaseModel):
    name = models.CharField(max_length=100, help_text="Enter the name of the exam series")
    description = models.TextField(blank=True, help_text="Enter a description for the exam series")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Series"
        verbose_name_plural = "Series"

    def get_absolute_url(self):
        return reverse_lazy("exams:series_detail", kwargs={"pk": self.pk})

    @staticmethod
    def get_list_url():
        return reverse_lazy("exams:series_list")

    def get_update_url(self):
        return reverse_lazy("exams:series_update", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse_lazy("exams:series_delete", kwargs={"pk": self.pk})


class Exam(BaseModel):
    series = models.ForeignKey(Series, on_delete=models.PROTECT, related_name="exams")
    subject = models.CharField(max_length=100, help_text="Enter the name of Subject")
    date = models.DateField(help_text="Enter the date of the exam")
    duration_minutes = models.PositiveIntegerField(help_text="Enter the duration of the exam in minutes")
    max_marks = models.PositiveIntegerField(help_text="Enter the maximum marks for the exam")
    pass_marks = models.PositiveIntegerField(help_text="Enter the pass marks for the exam")

    class Meta:
        ordering = ["date"]

    def __str__(self):
        return f"{self.series} {self.subject}"

    def get_absolute_url(self):
        return reverse_lazy("exams:exam_detail", kwargs={"pk": self.pk})

    @staticmethod
    def get_list_url():
        return reverse_lazy("exams:exam_list")

    def get_update_url(self):
        return reverse_lazy("exams:exam_update", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse_lazy("exams:exam_delete", kwargs={"pk": self.pk})


class StudentExam(BaseModel):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name="results")
    student = models.ForeignKey("students.Student", on_delete=models.PROTECT)
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    is_marked = models.BooleanField(default=False)

    class Meta:
        ordering = ["exam", "marks_obtained"]
        unique_together = ("exam", "student", "is_active")

    def __str__(self):
        return f"{self.student} - {self.exam} - Marks: {self.marks_obtained}"

    def get_absolute_url(self):
        return reverse_lazy("exams:student_exam_detail", kwargs={"pk": self.pk})

    @staticmethod
    def get_list_url():
        return reverse_lazy("exams:student_exam_list")

    def get_update_url(self):
        return reverse_lazy("exams:student_exam_update", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse_lazy("exams:student_exam_delete", kwargs={"pk": self.pk})

    def status(self):
        if self.is_marked:
            if self.marks_obtained < self.exam.pass_marks:
                return "Failed"
            else:
                return "Passed"
        else:
            return "Not Marked"
