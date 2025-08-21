from core.base import BaseAdmin
from django.contrib import admin

from .models import Course


@admin.register(Course)
class SeriesAdmin(BaseAdmin):
    list_display = ("teacher", "standard", "title")
    list_filter = ("teacher",)
    search_fields = ("teacher__first_name", "title")
