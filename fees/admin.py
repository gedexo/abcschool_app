from core.base import BaseAdmin
from django.contrib import admin

from .models import AdditionalFeeStudent


@admin.register(AdditionalFeeStudent)
class AdditionalFeeStudentAdmin(BaseAdmin):
    list_display = ("fee", "student", "amount", "due_date")
    list_filter = ("fee",)
    search_fields = ("student__first_name",)
