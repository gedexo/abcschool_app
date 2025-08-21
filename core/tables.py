from core.base import BaseTable
from django_tables2 import columns

from .models import Suggestion


class SuggestionTable(BaseTable):
    quickview = columns.TemplateColumn(template_name="app/partials/quick_view.html", orderable=False)

    class Meta:
        model = Suggestion
        fields = ("suggested_by", "quickview")
        attrs = {"class": "table border-0 star-student table-hover "}
