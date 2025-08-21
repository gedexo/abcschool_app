from django.urls import path

from . import views

app_name = "accounting"

urlpatterns = [
    path("accounts/", views.AccountListView.as_view(), name="account_list"),
    path("account/<str:pk>/", views.AccountDetailView.as_view(), name="account_detail"),
    path("new/account/", views.AccountCreateView.as_view(), name="account_create"),
    path(
        "account/<str:pk>/update/",
        views.AccountUpdateView.as_view(),
        name="account_update",
    ),
    path(
        "account/<str:pk>/delete/",
        views.AccountDeleteView.as_view(),
        name="account_delete",
    ),
    path(
        "expense_accounts/",
        views.ExpenseAccountListView.as_view(),
        name="expense_account_list",
    ),
    path(
        "expense_account/<str:pk>/",
        views.ExpenseAccountDetailView.as_view(),
        name="expense_account_detail",
    ),
    path(
        "new/expense_account/",
        views.ExpenseAccountCreateView.as_view(),
        name="expense_account_create",
    ),
    path(
        "expense_account/<str:pk>/update/",
        views.ExpenseAccountUpdateView.as_view(),
        name="expense_account_update",
    ),
    path(
        "expense_account/<str:pk>/delete/",
        views.ExpenseAccountDeleteView.as_view(),
        name="expense_account_delete",
    ),
    path("expenses/", views.ExpenseListView.as_view(), name="expense_list"),
    path("expense/<str:pk>/", views.ExpenseDetailView.as_view(), name="expense_detail"),
    path("new/expense/", views.ExpenseCreateView.as_view(), name="expense_create"),
    path(
        "expense/<str:pk>/update/",
        views.ExpenseUpdateView.as_view(),
        name="expense_update",
    ),
    path(
        "expense/<str:pk>/delete/",
        views.ExpenseDeleteView.as_view(),
        name="expense_delete",
    ),
    path(
        "expense_payments/",
        views.ExpensePaymentListView.as_view(),
        name="expense_payment_list",
    ),
    path(
        "expense_payment/<str:pk>/",
        views.ExpensePaymentDetailView.as_view(),
        name="expense_payment_detail",
    ),
    path(
        "new/expense_payment/<str:pk>/",
        views.ExpensePaymentCreateView.as_view(),
        name="expense_payment_create",
    ),
    path(
        "expense_payment/<str:pk>/update/",
        views.ExpensePaymentUpdateView.as_view(),
        name="expense_payment_update",
    ),
    path(
        "expense_payment/<str:pk>/delete/",
        views.ExpensePaymentDeleteView.as_view(),
        name="expense_payment_delete",
    ),
    path(
        "income_accounts/",
        views.IncomeAccountListView.as_view(),
        name="income_account_list",
    ),
    path(
        "income_account/<str:pk>/",
        views.IncomeAccountDetailView.as_view(),
        name="income_account_detail",
    ),
    path(
        "new/income_account/",
        views.IncomeAccountCreateView.as_view(),
        name="income_account_create",
    ),
    path(
        "income_account/<str:pk>/update/",
        views.IncomeAccountUpdateView.as_view(),
        name="income_account_update",
    ),
    path(
        "income_account/<str:pk>/delete/",
        views.IncomeAccountDeleteView.as_view(),
        name="income_account_delete",
    ),
    path("incomes/", views.IncomeListView.as_view(), name="income_list"),
    path("income/<str:pk>/", views.IncomeDetailView.as_view(), name="income_detail"),
    path("new/income/", views.IncomeCreateView.as_view(), name="income_create"),
    path(
        "income/<str:pk>/update/",
        views.IncomeUpdateView.as_view(),
        name="income_update",
    ),
    path(
        "income/<str:pk>/delete/",
        views.IncomeDeleteView.as_view(),
        name="income_delete",
    ),
    path("contras/", views.ContraListView.as_view(), name="contra_list"),
    path("contra/<str:pk>/", views.ContraDetailView.as_view(), name="contra_detail"),
    path("new/contra/", views.ContraCreateView.as_view(), name="contra_create"),
    path(
        "contra/<str:pk>/update/",
        views.ContraUpdateView.as_view(),
        name="contra_update",
    ),
    path(
        "contra/<str:pk>/delete/",
        views.ContraDeleteView.as_view(),
        name="contra_delete",
    ),
]
