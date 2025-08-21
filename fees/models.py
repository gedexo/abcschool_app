from core.base import BaseModel
from core.choices import ACADEMIC_YEAR_CHOICES, FEE_CHOICES
from django.db import models
from django.urls import reverse_lazy


class AdditionalFeeStudent(BaseModel):
    academic_year = models.CharField(max_length=128, choices=ACADEMIC_YEAR_CHOICES)
    fee = models.CharField(max_length=255, choices=FEE_CHOICES)
    fee_name = models.CharField(max_length=128, null=True, blank=True)
    student = models.ForeignKey(
        "students.Student",
        related_name="student_additional_fees",
        on_delete=models.PROTECT,
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        if self.fee == "other":
            return self.fee_name
        return self.fee

    def get_fee_name(self):
        if self.fee == "other":
            return self.fee_name
        return self.get_fee_display()

    class Meta:
        verbose_name = "Additional Fee student"
        verbose_name_plural = "Additional Fee studentes"
        ordering = ("academic_year", "-due_date")

    def get_absolute_url(self):
        return reverse_lazy("fees:additional_fee_student_detail", kwargs={"pk": self.pk})

    @staticmethod
    def get_list_url():
        return reverse_lazy("fees:additional_fee_student_list")

    def get_update_url(self):
        return reverse_lazy("fees:additional_fee_student_update", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse_lazy("fees:additional_fee_student_delete", kwargs={"pk": self.pk})
