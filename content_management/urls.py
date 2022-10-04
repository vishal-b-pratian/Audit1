from django.urls import path, include

urlpatterns = [
    path("", include("content_management.api.urls")),
]
