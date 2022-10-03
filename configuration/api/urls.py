from . import views
from django.urls import path

urlpatterns = [
    path("", views.getRoutes, name="get-routes"),
    path("users/", views.getUsersData, name="get-users"),
    path("company-details/", views.getCompanyDetailsData, name="get-company-details"),
    path("channels/<str:company_name>", views.getChannelsData, name="get-channels"),
    path("addChannel/", views.addChannel, name="addChannel"),
     path("add_channel_name/<str:channel_type_id>",views.addChannelName,name = "add-source"),
    path ("view_all_sources/<str:company_id>/",views.viewAllSources,name = "view-all-sources"),

    path ("view_source_by_id/<str:company_id>/<str:source_id>/",views.viewSourcebyID,name = "view-source-by-id"),

    path ("add_source/",views.addSource,name = "add-source"),

    path ("edit_source/",views.editSource,name = "edit-source"),
    #path("engagements/", views.addEngagement, name="add-engagement"),
    path("engagement-details/<str:company_id>", views.getEngagementDetails, name="get-company-details"),
    path("get_Urls_Channel_type/<str:company_name>/<str:engagement_type>/<str:channel_type>", views.getUrlDetailsChannelType, name="get-url-details-channelType"),
    path ("get_Urls_channels/<str:company_name>/<str:engagement_type>/<str:channel_name>",views.getUrlDetailsChannel,name = "get_url_details_channel"),
    path ("add_channel_type/<str:engagement_id>",views.add_channel_type,name = "add_channel_type"),
    path("activate_channel/",views.activateChannel,name = "activate_channel"),
    path("inactivate_channel/",views.inactivateChannel,name = "inactivate-channel"),
    path("activate_channel_type/",views.activateChannelType,name = "activate-channel-type"),
    path("inactivate_channel_type/",views.inactivateChannelType,name = "inactivate-channel-type"),
    path("view-message-architecture-content/<str:engagement_id>",views.viewMessageArchitectureContent,name ="view-message-architecture-content" )
    
]
