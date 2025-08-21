from decimal import ROUND_HALF_UP, Decimal

from core.base import BaseModel
from core.choices import ACADEMIC_YEAR_CHOICES, BLOOD_CHOICES, GENDER_CHOICES
from django.db import models
from django.urls import reverse_lazy
from versatileimagefield.fields import PPOIField, VersatileImageField


class Standard(BaseModel):
    name = models.CharField(max_length=50, help_text="Enter the standard name (e.g., Grade 1, Class 10)")
    description = models.TextField(blank=True, help_text="Enter a description for the standard")

    class Meta:
        ordering = ("created",)

    def __str__(self):
        return self.name

    @staticmethod
    def get_list_url():
        return reverse_lazy("students:standard_list")

    def get_absolute_url(self):
        return reverse_lazy("students:standard_detail", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse_lazy("students:standard_update", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse_lazy("students:standard_delete", kwargs={"pk": self.pk})


class Division(BaseModel):
    standard = models.ForeignKey(Standard, on_delete=models.PROTECT)
    name = models.CharField("Division", max_length=50, help_text="Enter the division name (e.g., A, B)")
    tutor = models.ForeignKey(
        "employees.Employee",
        on_delete=models.PROTECT,
        limit_choices_to={"user__usertype": "teacher"},
    )
    description = models.TextField(blank=True, help_text="Enter a description for the standard")

    class Meta:
        ordering = ("name",)
        unique_together = ("standard", "name")

    def __str__(self):
        return f"{self.standard} {self.name}"

    @staticmethod
    def get_list_url():
        return reverse_lazy("students:division_list")

    def get_absolute_url(self):
        return reverse_lazy("students:division_detail", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse_lazy("students:division_update", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse_lazy("students:division_delete", kwargs={"pk": self.pk})

    def student_count(self):
        return Student.objects.filter(division=self).count()


def get_next_admission_number():
    latest_admission_number = Student.objects.aggregate(models.Max("admission_number"))["admission_number__max"]
    if latest_admission_number is not None:
        next_admission_number = latest_admission_number + 1
    else:
        next_admission_number = 1
    return next_admission_number


class Student(BaseModel):
    user = models.OneToOneField(
        "accounts.User",
        on_delete=models.PROTECT,
        limit_choices_to={
            "is_active": True,
            "usertype": "student",
            "is_superuser": False,
        },
        related_name="student",
    )
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    admission_number = models.CharField(
        max_length=25,
        unique=True,
    )
    standard = models.ForeignKey("students.Standard", on_delete=models.PROTECT, null=True)
    division = models.ForeignKey(
        Division,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="students",
    )
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    blood_group = models.CharField(max_length=300, choices=BLOOD_CHOICES, blank=True, null=True)
    date_of_joining = models.DateField(null=True, blank=True)
    religion = models.CharField(max_length=128, null=True, blank=True)
    bus_no = models.PositiveIntegerField(null=True, blank=True)
    father_name = models.CharField(max_length=200, blank=True, null=True)
    mother_name = models.CharField(max_length=200, blank=True, null=True)
    primary_contact_number = models.CharField(max_length=15, blank=True, null=True)
    secondary_contact_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    photo = VersatileImageField(blank=True, null=True, upload_to="employees/photos/")
    ppoi = PPOIField("Image PPOI")

    class Meta:
        ordering = ("first_name",)

    def __str__(self):
        return f"{self.fullname} ({self.admission_number})"

    @staticmethod
    def get_list_url():
        return reverse_lazy("students:student_list")

    def get_absolute_url(self):
        return reverse_lazy("students:student_detail", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse_lazy("students:student_update", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse_lazy("students:student_delete", kwargs={"pk": self.pk})

    @property
    def fullname(self):
        return f"{self.first_name} {self.last_name}" if self.last_name else self.first_name
    
    def has_current_year_fee(self):
        from core.views import get_current_academic_year
        return self.academicyearstudentfee_set.filter(
            academic_year=get_current_academic_year(),   
            is_active=True
        ).exists()

    # @staticmethod
    # def next_admission_number():
    #     max_admission_no = Student.objects.aggregate(models.Max("admission_number"))
    #     max_admission_no_no = (
    #         max_admission_no["admission_number__max"]
    #         if max_admission_no["admission_number__max"] is not None
    #         else 0
    #     )
    #     return max_admission_no_no + 1


class AcademicYearStudentFee(BaseModel):
    academic_year = models.CharField(max_length=128, choices=ACADEMIC_YEAR_CHOICES)
    student = models.ForeignKey("students.Student", on_delete=models.CASCADE) 
    school_fee = models.DecimalField(max_digits=10, decimal_places=2)
    donation_fee = models.DecimalField("Admission Fee", max_digits=10, decimal_places=2)
    pta_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        unique_together = ("academic_year", "student", "is_active")
        ordering = ("academic_year",)

    def __str__(self):
        return f"{self.academic_year} {self.student}"

    @staticmethod
    def get_list_url():
        return reverse_lazy("students:academic_year_student_fee_list")

    def get_absolute_url(self):
        return reverse_lazy("students:academic_year_student_fee_detail", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse_lazy("students:academic_year_student_fee_update", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse_lazy("students:academic_year_student_fee_delete", kwargs={"pk": self.pk})

    def generate_fee_structure(self):
        # Assume course_duration_months is fixed to 8 for July to February
        course_duration_months = 8
        month_list = [
            "July",
            "August",
            "September",
            "October",
            "November",
            "December",
            "January",
            "February",
        ]
        fee_structure_list = []

        # Calculate monthly fee without rounding
        monthly_fee = Decimal((self.school_fee - self.donation_fee) / course_duration_months)

        # Calculate the rounded fee to the nearest multiple of 100
        rounded_fee = Decimal(round(monthly_fee, -2)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        # Calculate the rounding difference for the last month (February)
        rounding_difference = rounded_fee * course_duration_months - (self.school_fee - self.donation_fee)
        for i, month in enumerate(month_list):
            fee = rounded_fee if i < course_duration_months - 1 else (rounded_fee - rounding_difference).quantize(Decimal("0.01"))
            fee_structure = {"month": month, "fee": fee}
            fee_structure_list.append(fee_structure)
        return fee_structure_list

    def total_fee(self):
        additional_fees_qs = self.student.student_additional_fees.filter(academic_year=self.academic_year, is_active=True)
        additional_fees = sum([item.amount for item in additional_fees_qs])
        return self.school_fee + additional_fees

    def total_receipt(self):
        receipt_qs = self.student.student_fee_statement.filter(academic_year=self.academic_year, is_active=True)
        total_receipt_amount = sum([item.amount for item in receipt_qs])
        return total_receipt_amount

    def pending_fee(self):
        return self.total_fee() - self.total_receipt()


class StudentFeeStatement(BaseModel):
    academic_year = models.CharField(max_length=128, choices=ACADEMIC_YEAR_CHOICES)
    student = models.ForeignKey(
        "students.Student",
        on_delete=models.PROTECT,
        related_name="student_fee_statement",
    )
    account = models.ForeignKey(
        "accounting.Account",
        related_name="studentfeestatement_account",
        on_delete=models.PROTECT,
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    voucher_number = models.PositiveBigIntegerField("Receipt Number", null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Student Fee Receipt"
        verbose_name_plural = "StudentFee Receipts"

    def __str__(self):
        return f"{self.student} Fee Receipt"

    def get_absolute_url(self):
        return reverse_lazy("students:studentfeestatement_detail", kwargs={"pk": self.pk})

    @staticmethod
    def get_list_url():
        return reverse_lazy("students:studentfeestatement_list")

    def get_update_url(self):
        return reverse_lazy("students:studentfeestatement_update", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse_lazy("students:studentfeestatement_delete", kwargs={"pk": self.pk})
