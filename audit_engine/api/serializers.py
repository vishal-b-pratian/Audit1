import datetime
from rest_framework import serializers
from configuration import models as config_model


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = config_model.CompanyDetails
        fields = ["name", "compliance_score"]


class EngagementsSerializer(serializers.ModelSerializer):

    company = CompanySerializer()
    days_remaining = serializers.SerializerMethodField()

    class Meta:
        model = config_model.Engagement
        fields = ["company", "days_remaining"]

    def get_days_remaining(self, obj):
        time_diff = obj.end_Date - datetime.datetime.now(datetime.timezone.utc)
        if time_diff.total_seconds() < 0:
            return "Ended"
        return f"{time_diff.days} Days to go"
