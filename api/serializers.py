from configuration import models as config_models
from rest_framework import serializers
from django.contrib.auth import models as auth_models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = auth_models.User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "is_staff",
            "is_active",
            "date_joined",
        ]
        read_only_fields = ["id", "is_staff", "date_joined"]


class CompanyDetailsSerializer(serializers.ModelSerializer):

    user = UserSerializer()

    class Meta:
        model = config_models.CompanyDetails
        fields = ["id", "user", "name", "created", "updated", "is_active"]
        read_only_fields = ["id", "user", "created", "updated"]


class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = config_models.Channel
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
        model = config_models.ChannelData
        fields = [
            "id",
            "channel",
            "scraped_data",
            "processed_data",
            "created",
            "updated",
        ]
        read_only_fields = ["id", "channel", "created", "updated"]
