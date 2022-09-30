from . import views
from django.urls import path

urlpatterns = [
    path(
        "create-channel-data/<uuid:channel_id>",
        views.CreateChannelData.as_view(),
        name="create-channel-data",
    ),
]
