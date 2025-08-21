from core.base import BaseTable

from .models import Course


class CourseTable(BaseTable):
    class Meta:
        model = Course
        fields = ("title", "standard", "teacher")
        attrs = {"class": "table border-0 star-student table-hover "}
