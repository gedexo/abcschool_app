from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = (
    [
        path("admin/", admin.site.urls),
        path("", include("core.urls", namespace="core")),
        path("accounts/", include("accounts.urls", namespace="accounts")),
        path("employees/", include("employees.urls", namespace="employees")),
        path("students/", include("students.urls", namespace="students")),
        path("accounting/", include("accounting.urls", namespace="accounting")),
        path("reports/", include("reports.urls", namespace="reports")),
        path("fees/", include("fees.urls", namespace="fees")),
        path("exams/", include("exams.urls", namespace="exams")),
        path("tasks/", include("tasks.urls", namespace="tasks")),
        path("courses/", include("courses.urls", namespace="courses")),
        path("hrms/", include("hrms.urls", namespace="hrms")),
        path("accounts/", include("registration.backends.default.urls")),
        path("tinymce/", include("tinymce.urls")),
        path(
            "sitemap.xml",
            TemplateView.as_view(template_name="sitemap.xml", content_type="text/xml"),
        ),
        path(
            "robots.txt",
            TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
        ),
    ]
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)

admin.site.site_header = "ABC School Administration"
admin.site.site_title = "ABC School Admin Portal"
admin.site.index_title = "Welcome to ABC School Admin Portal"
