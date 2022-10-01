from . import views
from . import engagements_views, audit_views
from django.urls import path

urlpatterns = [
    path("", views.getRoutes, name="get-routes"),
    path("status/", views.getStatus, name="get-status"),
    path("compliance-score/", views.getOverallScore, name="get-compliance-score"),
    path("get-engagements/", views.getEngagements.as_view()),
    path("get-engagements/get", engagements_views.getEngagementDetails),
    path("create-engagements", engagements_views.createEngagement.as_view()),
    path("edit-engagements", engagements_views.editEngagement),
    path("delete-engagements", engagements_views.deleteEngagement),
    path("company-engagements", engagements_views.companyEngagements),
    path("company-detailed-audit", audit_views.getAuditDetails),
]
