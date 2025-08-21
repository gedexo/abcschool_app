from django.contrib import admin

from .base import BaseAdmin
from .models import Suggestion


@admin.register(Suggestion)
class SuggestionAdmin(BaseAdmin):
    list_display = ("suggested_by",)
    search_fields = ("suggested_by__first_name",)
