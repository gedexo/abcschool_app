from core import mixins
from django.db.models import Q
from django.urls import reverse_lazy

from . import tables
from .models import (
    Account,
    Contra,
    Expense,
    ExpenseAccount,
    ExpensePayment,
    Income,
    IncomeAccount,
)


class AccountListView(mixins.HybridListView):
    model = Account
    table_class = tables.AccountTable
    filterset_fields = ["account_name", "decription"]
    permissions = (
        "management",
        "accountant",
    )

    def get_queryset(self):
        base_queryset = super().get_queryset()
        if self.request.user.usertype == "branch":
            base_queryset = base_queryset.filter(user=self.request.user)
        return base_queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Accounts"
        context["is_accounts"] = True
        context["can_add"] = mixins.check_access(self.request, ("accountant"))
        context["new_link"] = reverse_lazy("accounting:account_create")
        return context


class AccountDetailView(mixins.HybridDetailView):
    model = Account
    permissions = (
        "management",
        "accountant",
    )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Account"
        return context


class AccountCreateView(mixins.HybridCreateView):
    model = Account
    exclude = ("is_active", "creator")
    permissions = ("accountant",)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = " Account"
        return context


class AccountUpdateView(mixins.HybridUpdateView):
    model = Account
    permissions = ("accountant",)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Update Account"
        return context


class AccountDeleteView(mixins.HybridDeleteView):
    model = Account
    permissions = ("accountant",)


class ExpenseAccountListView(mixins.HybridListView):
    model = ExpenseAccount
    table_class = tables.ExpenseAccountTable
    filterset_fields = {"name": ["icontains"]}
    permissions = (
        "management",
        "accountant",
    )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Expense Accounts"
        context["is_expense_account"] = True
        context["can_add"] = mixins.check_access(self.request, ("accountant"))
        context["new_link"] = reverse_lazy("accounting:expense_account_create")
        return context


class ExpenseAccountDetailView(mixins.HybridDetailView):
    model = ExpenseAccount
    permissions = (
        "management",
        "accountant",
    )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Expense Account"
        return context


class ExpenseAccountCreateView(mixins.HybridCreateView):
    model = ExpenseAccount
    exclude = ("creator", "is_active")
    permissions = ("accountant",)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = " Expense Account"
        return context


class ExpenseAccountUpdateView(mixins.HybridUpdateView):
    model = ExpenseAccount
    permissions = ("accountant",)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Update Expense Account"
        return context


class ExpenseAccountDeleteView(mixins.HybridDeleteView):
    model = ExpenseAccount
    permissions = ("accountant",)


class ExpenseListView(mixins.HybridListView):
    model = Expense
    table_class = tables.ExpenseTable
    filterset_fields = {
        "expense_account": ["exact"],
        "date": ["lte"],
    }
    permissions = (
        "management",
        "accountant",
    )

    def get_queryset(self):
        base_queryset = super(ExpenseListView, self).get_queryset()
        if self.request.user.usertype == "branch":
            base_queryset = base_queryset.filter(expense_against=self.request.user)
        return base_queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Expenses"
        context["is_expenses"] = True
        context["can_add"] = mixins.check_access(self.request, ("accountant"))
        context["new_link"] = reverse_lazy("accounting:expense_create")
        return context


class ExpenseDetailView(mixins.HybridDetailView):
    model = Expense
    permissions = (
        "management",
        "accountant",
    )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Expense"
        return context


class ExpenseCreateView(mixins.HybridCreateView):
    model = Expense
    exclude = ("creator", "is_active")
    permissions = ("accountant",)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Expense"
        return context


class ExpenseUpdateView(mixins.HybridUpdateView):
    model = Expense
    permissions = ("accountant",)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Expense"
        return context


class ExpenseDeleteView(mixins.HybridDeleteView):
    model = Expense
    permissions = ("accountant",)


class ExpensePaymentListView(mixins.HybridListView):
    model = ExpensePayment
    table_class = tables.ExpensePaymentTable
    filterset_fields = {"expense": ["exact"]}
    permissions = (
        "management",
        "accountant",
    )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Expense Payments"
        context["is_expense_payments"] = True
        context["new_link"] = reverse_lazy("accounting:expense_payment_create")
        return context


class ExpensePaymentDetailView(mixins.HybridDetailView):
    model = ExpensePayment
    permissions = (
        "management",
        "accountant",
    )


class ExpensePaymentCreateView(mixins.HybridCreateView):
    model = ExpensePayment
    exclude = ("creator", "is_active", "expense")
    permissions = ("accountant",)

    def form_valid(self, form):
        expense = self.kwargs.get("pk")
        form.instance.expense = Expense.objects.get(pk=expense)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = " Expense Payment"
        return context


class ExpensePaymentUpdateView(mixins.HybridUpdateView):
    model = ExpensePayment
    permissions = ("accountant",)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Expense Payment"
        return context


class ExpensePaymentDeleteView(mixins.HybridDeleteView):
    model = ExpensePayment
    permissions = ("accountant",)


class IncomeAccountListView(mixins.HybridListView):
    model = IncomeAccount
    table_class = tables.IncomeAccountTable
    filterset_fields = {"name": ["icontains"], "description": ["icontains"]}
    permissions = (
        "management",
        "accountant",
    )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Income Account"
        context["is_income_accounts"] = True
        context["can_add"] = mixins.check_access(self.request, ("accountant",))
        context["new_link"] = reverse_lazy("accounting:income_account_create")
        return context


class IncomeAccountDetailView(mixins.HybridDetailView):
    model = IncomeAccount
    permissions = (
        "management",
        "accountant",
    )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Income Account"
        return context


class IncomeAccountCreateView(mixins.HybridCreateView):
    model = IncomeAccount
    exclude = ("is_active", "creator")
    permissions = ("accountant",)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = " Income Account"
        return context


class IncomeAccountUpdateView(mixins.HybridUpdateView):
    model = IncomeAccount
    permissions = ("accountant",)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Income Account"
        return context


class IncomeAccountDeleteView(mixins.HybridDeleteView):
    model = IncomeAccount
    permissions = ("accountant",)


class IncomeListView(mixins.HybridListView):
    model = Income
    table_class = tables.IncomeTable
    filterset_fields = ["income_account", "amount"]
    permissions = (
        "management",
        "accountant",
    )

    def get_queryset(self):
        base_queryset = super().get_queryset()
        if self.request.user.usertype == "branch":
            base_queryset = base_queryset.filter(income_against=self.request.user)
        return base_queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Incomes"
        context["is_incomes"] = True
        context["can_add"] = mixins.check_access(self.request, ("management", "accountant"))
        context["new_link"] = reverse_lazy("accounting:income_create")
        return context


class IncomeDetailView(mixins.HybridDetailView):
    model = Income
    permissions = ("management", "accountant")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Income "
        return context


class IncomeCreateView(mixins.HybridCreateView):
    model = Income
    exclude = ("creator", "is_active")
    permissions = ("accountant",)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = " Income"
        return context


class IncomeUpdateView(mixins.HybridUpdateView):
    model = Income
    permissions = ("accountant",)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Income "
        return context


class IncomeDeleteView(mixins.HybridDeleteView):
    model = Income
    permissions = ("accountant",)


class ContraListView(mixins.HybridListView):
    model = Contra
    table_class = tables.ContraTable
    filterset_fields = {
        "from_account": ["exact"],
        "to_account": ["exact"],
    }
    permissions = (
        "management",
        "accountant",
    )

    def get_queryset(self):
        base_queryset = super().get_queryset()
        if self.request.user.usertype == "branch":
            base_queryset = base_queryset.filter(Q(from_account__user=self.request.user) | Q(to_account__user=self.request.user))
        return base_queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Contra"
        context["is_contra"] = True
        context["can_add"] = mixins.check_access(self.request, ("accountant",))
        context["new_link"] = reverse_lazy("accounting:contra_create")
        return context


class ContraDetailView(mixins.HybridDetailView):
    model = Contra
    permissions = ("management", "accountant")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Contra"
        return context


class ContraCreateView(mixins.HybridCreateView):
    model = Contra
    permissions = ("accountant",)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = " Contra"
        return context


class ContraUpdateView(mixins.HybridUpdateView):
    model = Contra
    permissions = ("accountant",)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Contra"
        return context


class ContraDeleteView(mixins.HybridDeleteView):
    model = Contra
    permissions = ("accountant",)
