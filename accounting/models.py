from datetime import datetime

from core.base import BaseModel
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse_lazy


class Account(BaseModel):
    user = models.ForeignKey(
        "accounts.User",
        on_delete=models.PROTECT,
        limit_choices_to={"usertype__in": ("branch", "accountant")},
    )
    account_name = models.CharField(max_length=100)
    decription = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.account_name}"

    def get_absolute_url(self):
        return reverse_lazy("accounting:account_detail", kwargs={"pk": self.pk})

    @staticmethod
    def get_list_url():
        return reverse_lazy("accounting:account_list")

    def get_update_url(self):
        return reverse_lazy("accounting:account_update", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse_lazy("accounting:account_delete", kwargs={"pk": self.pk})

    def totoal_credits(self):
        fee_receipt_qs = self.studentfeestatement_account.filter(is_active=True)
        total_fee = sum([item.amount for item in fee_receipt_qs])
        other_income_qs = self.other_income.filter(is_active=True)
        total_other_income = sum([item.amount for item in other_income_qs])
        return total_fee + total_other_income

    def total_debits(self):
        employee_payment_qs = self.employee_payment_account.filter(is_active=True)
        total_employee_payment = sum([item.amount for item in employee_payment_qs])
        other_expense_qs = self.other_expense.filter(is_active=True)
        total_other_expense = sum([item.amount for item in other_expense_qs])
        return total_employee_payment + total_other_expense

    def balance(self):
        return self.totoal_credits() - self.total_debits()

    # today report
    def today_credit(self):
        fee_receipt_qs = self.studentfeestatement_account.filter(is_active=True, date=datetime.today())
        total_fee = sum([item.amount for item in fee_receipt_qs])
        other_income_qs = self.other_income.filter(is_active=True, date=datetime.today())
        total_other_income = sum([item.amount for item in other_income_qs])
        return total_fee + total_other_income

    def today_expense(self):
        employee_payment_qs = self.employee_payment_account.filter(is_active=True, date=datetime.today())
        total_employee_payment = sum([item.amount for item in employee_payment_qs])
        other_expense_qs = self.other_expense.filter(is_active=True, date=datetime.today())
        total_other_expense = sum([item.amount for item in other_expense_qs])
        return total_employee_payment + total_other_expense


class ExpenseAccount(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse_lazy("accounting:expense_account_detail", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse_lazy("accounting:expense_account_update", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse_lazy("accounting:expense_account_delete", kwargs={"pk": self.pk})

    @staticmethod
    def get_list_url():
        return reverse_lazy("accounting:expense_account_list")


class Expense(BaseModel):
    expense_account = models.ForeignKey(ExpenseAccount, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    description = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ("-date",)

    def __str__(self):
        return f"Expense on {self.date}: {self.amount} for {self.expense_account}."

    def get_absolute_url(self):
        return reverse_lazy("accounting:expense_detail", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse_lazy("accounting:expense_update", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse_lazy("accounting:expense_delete", kwargs={"pk": self.pk})

    @staticmethod
    def get_list_url():
        return reverse_lazy("accounting:expense_list")

    def get_payment_create_url(self):
        return reverse_lazy("accounting:expense_payment_create", kwargs={"pk": self.pk})

    def total_paid(self):
        payments = ExpensePayment.objects.filter(is_active=True, expense=self)
        return sum([item.amount for item in payments])

    def balance(self):
        return self.amount - self.total_paid()


def get_next_voucher_number():
    max_voucher_number = ExpensePayment.objects.aggregate(models.Max("voucher_number"))["voucher_number__max"]
    if max_voucher_number is not None:
        next_voucher_number = max_voucher_number + 1
    else:
        next_voucher_number = 1
    return next_voucher_number


class ExpensePayment(BaseModel):
    expense = models.ForeignKey(Expense, on_delete=models.PROTECT)
    debit_account = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        related_name="other_expense",
        limit_choices_to={
            "is_active": True,
        },
    )
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    voucher_number = models.PositiveBigIntegerField(
        "Payment Voucher",
        null=True,
        blank=True,
        unique=True,
        default=get_next_voucher_number,
    )

    def __str__(self):
        return f"Payment for Expense on {self.expense.date} - Voucher: {self.voucher_number}, Debited from: {self.debit_account}."

    def get_absolute_url(self):
        return reverse_lazy("accounting:expense_payment_detail", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse_lazy("accounting:expense_payment_update", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse_lazy("accounting:expense_payment_delete", kwargs={"pk": self.pk})

    @staticmethod
    def get_list_url():
        return reverse_lazy("accounting:expense_payment_list")


class IncomeAccount(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse_lazy("accounting:income_account_detail", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse_lazy("accounting:income_account_update", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse_lazy("accounting:income_account_delete", kwargs={"pk": self.pk})

    @staticmethod
    def get_list_url():
        return reverse_lazy("accounting:income_account_list")


class Income(BaseModel):
    income_account = models.ForeignKey(IncomeAccount, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    credit_account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name="other_income")
    date = models.DateField()
    voucher_number = models.PositiveBigIntegerField("Receipt Number", null=True, blank=True, unique=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ("-date",)

    def __str__(self):
        return f"Income: {self.amount} for {self.income_account} on {self.date}"

    def get_absolute_url(self):
        return reverse_lazy("accounting:income_detail", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse_lazy("accounting:income_update", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse_lazy("accounting:income_delete", kwargs={"pk": self.pk})

    @staticmethod
    def get_list_url():
        return reverse_lazy("accounting:income_list")


class Contra(BaseModel):
    from_account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name="from_account")
    to_account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name="to_account")
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    date = models.DateField()
    description = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"Transaction from {self.from_account} to {self.to_account}"

    def clean(self):
        if self.from_account == self.to_account:
            raise ValidationError("Account cannot be same")
        if self.from_account.user != self.to_account.user:
            raise ValidationError("From Account and To Account must belong to the same user account.")

    def get_absolute_url(self):
        return reverse_lazy("accounting:contra_detail", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse_lazy("accounting:contra_update", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse_lazy("accounting:contra_delete", kwargs={"pk": self.pk})

    @staticmethod
    def get_list_url():
        return reverse_lazy("accounting:contra_list")
