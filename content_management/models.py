import uuid
from django.db import models
from configuration import models as config_models

# Create your models here.


class Channel(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, verbose_name="Channel Id", primary_key=True, editable=True
    )
    type_name = models.ForeignKey(
        config_models.ChannelType, on_delete=models.CASCADE, related_name="type"
    )
    company = models.ForeignKey(
        config_models.CompanyDetails, on_delete=models.CASCADE, null=True
    )
    url = models.URLField(
        verbose_name="Channel Url", unique=True, null=True, max_length=200
    )
    weightage = models.FloatField(verbose_name="Weightage", null=True, default=1.0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    compliance_score = models.FloatField(verbose_name="Compliance Score", default=0)

    def __str__(self):
        return f"{self.company} -> {self.url}"


class ChannelData(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, verbose_name="Data Id", primary_key=True, editable=True
    )
    channel = models.ForeignKey("Channel", on_delete=models.CASCADE)
    scraped_data = models.TextField(verbose_name="Scarped Data", null=True)
    processed_data = models.TextField(
        verbose_name="Processed Data", null=True, blank=True
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.channel} data"
