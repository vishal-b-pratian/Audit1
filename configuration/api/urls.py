from . import views
from django.urls import path

urlpatterns = [
    path("", views.getRoutes, name="get-routes"),
    path("users/", views.getUsersData, name="get-users"),
    path("company-details/", views.getCompanyDetailsData, name="get-company-details"),
]
