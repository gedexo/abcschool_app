from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("suggestions/", views.SuggestionListView.as_view(), name="suggestion_list"),
    path(
        "suggestion/<str:pk>/",
        views.SuggestionDetailView.as_view(),
        name="suggestion_detail",
    ),
    path(
        "new/suggestion/",
        views.SuggestionCreateView.as_view(),
        name="suggestion_create",
    ),
    path(
        "suggestion/<str:pk>/update/",
        views.SuggestionUpdateView.as_view(),
        name="suggestion_update",
    ),
    path(
        "suggestion/<str:pk>/delete/",
        views.SuggestionDeleteView.as_view(),
        name="suggestion_delete",
    ),
]
