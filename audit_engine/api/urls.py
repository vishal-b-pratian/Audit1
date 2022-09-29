from . import views
from django.urls import path

urlpatterns = [
    path("", views.getRoutes, name="get-routes"),
    path("status/", views.getStatus, name="get-status"),
    path("compliance-score/", views.getOverallScore, name="get-compliance-score"),
    path("get-engagements/", views.getEngagements.as_view()),
]
