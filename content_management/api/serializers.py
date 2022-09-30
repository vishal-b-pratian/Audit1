from rest_framework import serializers
from content_management import models as component_models


class ChannelDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = component_models
        fields = [
            "id",
            "channel",
            "scraped_data",
            "processed_data",
            "created",
            "updated",
        ]
        read_only_fields = ["id", "channel", "created", "updated"]
