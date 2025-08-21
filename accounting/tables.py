from core.base import BaseTable
from django_tables2 import columns

from .models import (
    Account,
    Contra,
    Expense,
    ExpenseAccount,
    ExpensePayment,
    Income,
    IncomeAccount,
)


class ExpensePaymentTable(BaseTable):
    class Meta:
        model = ExpensePayment
        fields = ("debit_account", "date", "amount", "voucher_number")
        attrs = {"class": "table border-0 star-student table-hover "}


class AccountTable(BaseTable):
    account_name = columns.Column(linkify=True)
    totoal_credits = columns.Column(orderable=False)
    total_debits = columns.Column(orderable=False)
    balance = columns.Column(orderable=False)

    class Meta:
        model = Account
        fields = ("account_name", "totoal_credits", "total_debits", "balance")
        attrs = {"class": "table border-0 star-student table-hover "}


class ExpenseAccountTable(BaseTable):
    name = columns.Column(linkify=True)

    class Meta:
        model = ExpenseAccount
        fields = ("name",)
        attrs = {"class": "table border-0 star-student table-hover "}


class ExpenseTable(BaseTable):
    action = columns.TemplateColumn(
        """
        <div class="dropdown ">
            <button class="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton" data-bs-toggle="dropdown">
            Action
            </button>
            <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton">
                <li><a class="dropdown-item" href="{{record.get_absolute_url}}">View </a></li>
                <li><a class="dropdown-item" href="{{record.get_update_url}}">Edit </a></li>
                <li><a class="dropdown-item" href="{{record.get_payment_create_url}}">New Payment </a></li>
                <li><a class="dropdown-item" href="{% url 'accounting:expense_payment_list' %}?expense={{record.pk}}">View Payments</a></li>
               
            </ul>
        </div>
         """,
        orderable=False,
    )
    expense_account = columns.Column(linkify=True)
    total_paid = columns.Column(orderable=False)
    balance = columns.Column(orderable=False)

    class Meta:
        model = Expense
        fields = ("expense_account", "date", "amount", "total_paid", "balance")
        attrs = {"class": "table border-0 star-student table-hover "}


class IncomeAccountTable(BaseTable):
    name = columns.Column(linkify=True)

    class Meta:
        model = IncomeAccount
        fields = ("name", "description")
        attrs = {"class": "table border-0 star-student table-hover "}


class IncomeTable(BaseTable):
    income_account = columns.Column(linkify=True)

    class Meta:
        model = Income
        fields = (
            "income_account",
            "amount",
            "credit_account",
            "date",
            "voucher_number",
        )
        attrs = {"class": "table border-0 star-student table-hover "}


class ContraTable(BaseTable):
    from_account = columns.Column(linkify=True)

    class Meta:
        model = Contra
        fields = ("from_account", "to_account", "amount", "amount", "date")
        attrs = {"class": "table border-0 star-student table-hover "}
