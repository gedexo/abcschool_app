from core.base import BaseModel
from core.choices import (
    BLOOD_CHOICES,
    EMPLOYMENT_TYPE_CHOICES,
    GENDER_CHOICES,
    MARITAL_CHOICES,
    MONTH_CHOICES,
    RESIDENCE_CHOICES,
    YEAR_CHOICES,
)
from django.db import models
from django.urls import reverse_lazy
from versatileimagefield.fields import PPOIField, VersatileImageField


class Designation(BaseModel):
    name = models.CharField(max_length=128)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse_lazy("employees:designation_detail", kwargs={"pk": self.pk})

    @staticmethod
    def get_list_url():
        return reverse_lazy("employees:designation_list")

    def get_update_url(self):
        return reverse_lazy("employees:designation_update", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse_lazy("employees:designation_delete", kwargs={"pk": self.pk})


class Department(BaseModel):
    name = models.CharField(max_length=128)
    description = models.TextField(blank=True, null=True)
    department_lead = models.ForeignKey(
        "employees.Employee",
        on_delete=models.PROTECT,
        limit_choices_to={"is_active": True},
        blank=True,
        null=True,
        related_name="department_list",
    )

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse_lazy("employees:department_detail", kwargs={"pk": self.pk})

    @staticmethod
    def get_list_url():
        return reverse_lazy("employees:department_list")

    def get_update_url(self):
        return reverse_lazy("employees:department_update", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse_lazy("employees:department_delete", kwargs={"pk": self.pk})


class Employee(BaseModel):
    user = models.OneToOneField(
        "accounts.User",
        on_delete=models.PROTECT,
        limit_choices_to={
            "is_active": True,
            "usertype__in": ("management", "teacher", "worker", "accountant"),
            "is_superuser": False,
        },
        related_name="employee",
    )
    employee_id = models.CharField(max_length=128, unique=True)
    first_name = models.CharField(max_length=300)
    middle_name = models.CharField(max_length=128, blank=True, null=True)
    last_name = models.CharField(max_length=128, blank=True, null=True)
    gender = models.CharField(max_length=128, choices=GENDER_CHOICES, blank=True, null=True)
    marital_status = models.CharField(max_length=128, choices=MARITAL_CHOICES, blank=True, null=True)
    personal_email = models.EmailField(max_length=128, blank=True, null=True)
    mobile = models.CharField(max_length=128, blank=True, null=True)
    whatsapp = models.CharField(max_length=128, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    religion = models.CharField(max_length=128, blank=True, null=True)
    photo = VersatileImageField(blank=True, null=True, upload_to="employees/photos/")
    ppoi = PPOIField("Image PPOI")

    # Company Info
    official_email = models.EmailField(max_length=128, blank=True, null=True)
    department = models.ForeignKey(
        "employees.Department",
        on_delete=models.PROTECT,
        limit_choices_to={"is_active": True},
    )
    designation = models.ForeignKey(
        "employees.Designation",
        on_delete=models.PROTECT,
        limit_choices_to={"is_active": True},
    )

    # Parent Info
    father_name = models.CharField(max_length=128, blank=True, null=True)
    father_mobile = models.CharField(max_length=128, blank=True, null=True)
    mother_name = models.CharField(max_length=128, blank=True, null=True)
    guardian_name = models.CharField(max_length=128, blank=True, null=True)
    guardian_mobile = models.CharField(max_length=128, blank=True, null=True)
    relationship_with_employee = models.CharField(max_length=128, blank=True, null=True)

    # Dates
    date_of_joining = models.DateField(blank=True, null=True)
    date_of_confirmation = models.DateField(blank=True, null=True)

    # Residence Info
    type_of_residence = models.CharField(max_length=128, choices=RESIDENCE_CHOICES, blank=True, null=True)
    residence_name = models.CharField(max_length=128, blank=True, null=True)
    residential_address = models.TextField(blank=True, null=True)
    residence_contact = models.CharField(max_length=128, blank=True, null=True)
    residential_postal_code = models.CharField(max_length=128, blank=True, null=True)
    permanent_address = models.TextField(blank=True, null=True)
    permanent_postal_code = models.CharField(max_length=128, blank=True, null=True)

    # Account Info
    bank_name = models.CharField(max_length=128, blank=True, null=True)
    account_name = models.CharField(max_length=128, blank=True, null=True)
    account_number = models.CharField("Bank Account Number", max_length=128, blank=True, null=True)
    ifsc_code = models.CharField("Bank IFSC Code", max_length=128, blank=True, null=True)
    bank_branch = models.CharField(max_length=128, blank=True, null=True)
    pan_number = models.CharField("PAN Card Number", max_length=128, blank=True, null=True)
    employment_type = models.CharField(max_length=128, choices=EMPLOYMENT_TYPE_CHOICES, blank=True, null=True)

    # Emergency Info
    blood_group = models.CharField(max_length=300, choices=BLOOD_CHOICES, blank=True, null=True)

    class Meta:
        verbose_name = "Employee"
        verbose_name_plural = "Employees"
        ordering = ["last_name", "first_name"]

    def __str__(self):
        return self.fullname

    def get_absolute_url(self):
        return reverse_lazy("employees:employee_detail", kwargs={"pk": self.pk})

    @staticmethod
    def get_list_url():
        return reverse_lazy("employees:employee_list")

    def get_update_url(self):
        return reverse_lazy("employees:employee_update", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse_lazy("employees:employee_delete", kwargs={"pk": self.pk})

    @property
    def fullname(self):
        return f"{self.first_name} {self.last_name}" if self.last_name else self.first_name


class EmployeePayroll(BaseModel):
    employee = models.ForeignKey(
        "employees.Employee",
        on_delete=models.PROTECT,
    )
    amount = models.DecimalField("Salary", max_digits=10, decimal_places=2)
    month = models.IntegerField(choices=MONTH_CHOICES)
    year = models.IntegerField(choices=YEAR_CHOICES)
    remark = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Employee Payroll"
        verbose_name_plural = "Employee Payrolls"

    def __str__(self):
        return f"{self.employee} {self.get_month_display()} - {self.year}"

    def get_absolute_url(self):
        return reverse_lazy("employees:employeepayroll_detail", kwargs={"pk": self.pk})

    @staticmethod
    def get_list_url():
        return reverse_lazy("employees:employeepayroll_list")

    def get_update_url(self):
        return reverse_lazy("employees:employeepayroll_update", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse_lazy("employees:employeepayroll_delete", kwargs={"pk": self.pk})


class EmployeePayment(BaseModel):
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    account = models.ForeignKey(
        "accounting.Account",
        related_name="employee_payment_account",
        on_delete=models.PROTECT,
    )
    date = models.DateField()
    voucher_number = models.PositiveBigIntegerField("Payment Voucher", unique=True, null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.employee}"

    class Meta:
        ordering = ("-date",)

    def get_absolute_url(self):
        return reverse_lazy("employees:employeepayment_detail", kwargs={"pk": self.pk})

    @staticmethod
    def get_list_url():
        return reverse_lazy("employees:employeepayment_list")

    def get_update_url(self):
        return reverse_lazy("employees:employeepayment_update", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse_lazy("employees:employeepayment_delete", kwargs={"pk": self.pk})
