from core.base import BaseAdmin
from django.contrib import admin

from .models import (
    Account,
    Contra,
    Expense,
    ExpenseAccount,
    ExpensePayment,
    Income,
    IncomeAccount,
)


@admin.register(Account)
class AccountAdmin(BaseAdmin):
    list_display = ("user", "account_name", "decription")
    list_filter = ("user",)  # Add more filter fields as needed
    search_fields = ("account_name", "decription")


@admin.register(ExpenseAccount)
class ExpenseAccountAdmin(BaseAdmin):
    list_display = ("name", "description")
    search_fields = ("name", "description")


@admin.register(Expense)
class ExpenseAdmin(BaseAdmin):
    list_display = ("expense_account", "amount", "date")
    search_fields = ("debit_account__user__first_name",)


@admin.register(ExpensePayment)
class ExpensePaymentAdmin(BaseAdmin):
    list_display = ("expense", "debit_account", "date", "amount")


@admin.register(IncomeAccount)
class IncomeAccountAdmin(BaseAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)


@admin.register(Income)
class IncomeAdmin(BaseAdmin):
    list_display = (
        "income_account",
        "amount",
        "credit_account",
        "date",
        "voucher_number",
    )
    list_filter = (
        "income_account",
        "credit_account",
    )


@admin.register(Contra)
class ContraAdmin(BaseAdmin):
    list_display = ("from_account", "to_account", "amount", "date", "description")
    list_filter = ("from_account", "to_account")  # Add more filter fields as needed
    search_fields = ("amount", "description")
