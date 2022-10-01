from . import views
from django.urls import path

urlpatterns = [
    path("", views.getRoutes, name="get-routes"),
    path("users/", views.getUsersData, name="get-users"),
    path("company-details/", views.getCompanyDetailsData, name="get-company-details"),
    path("channels/<str:company_name>", views.getChannelsData, name="get-channels"),
    path("engagements/", views.addEngagement, name="add-engagement"),
    path("engagement-details/<str:company_name>", views.getEngagementDetails, name="get-company-details"),
    path("get_Urls_Channel_type/<str:company_name>/<str:engagement_type>/<str:channel_type>", views.getUrlDetailsChannelType, name="get-url-details-channelType"),
    path ("get_Urls_channels/<str:company_name>/<str:engagement_type>/<str:channel_name>",views.getUrlDetailsChannel,name = "get_url_details_channel")
    
]
