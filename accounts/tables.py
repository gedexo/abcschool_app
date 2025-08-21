from core.base import BaseTable
from django_tables2 import columns

from .models import User


class UserTable(BaseTable):
    username = columns.Column(linkify=True)
    fullname = columns.Column(order_by="first_name")
    date_joined = columns.DateTimeColumn(format="d/m/y")
    created = None

    class Meta:
        model = User
        fields = (
            "username",
            "fullname",
            "usertype",
            "date_joined",
            "last_login",
            "is_active",
            "is_staff",
            "is_superuser",
        )
        attrs = {"class": "table border-0 star-student table-hover "}
