from . import views
from django.urls import path

urlpatterns = [
    path("", views.getRoutes, name="get-routes"),
    path("users/", views.getUsersData, name="get-users"),
    path("company-details/", views.getCompanyDetailsData, name="get-company-details"),
    path(
        "generate-score-card/",
        views.GenerateScoreCard.as_view(),
        name="generate-score-card",
    ),
    path("create-channel/", views.CreateChannel.as_view(), name="create-channel"),
    path(
        "create-channel-data/<uuid:channel_id>",
        views.CreateChannelData.as_view(),
        name="create-channel-data",
    ),
]
