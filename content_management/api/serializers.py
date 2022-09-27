from rest_framework import serializers
from content_management import models as component_models


class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = component_models.Channel
        fields = [
            "id",
            "type_name",
            "company",
            "url",
            "weightage",
            "created",
            "updated",
        ]
        read_only_fields = [
            "id",
            "company",
            "created",
            "updated",
        ]


class ChannelDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = component_models.ChannelData
        fields = [
            "id",
            "channel",
            "scraped_data",
            "processed_data",
            "created",
            "updated",
        ]
        read_only_fields = ["id", "channel", "created", "updated"]
