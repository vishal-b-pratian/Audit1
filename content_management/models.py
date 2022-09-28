import uuid
from django.db import models
from audit_engine import models as audit_models
from configuration import models as config_models

# Create your models here.


class Channel(models.Model):
    """
    Table is used to store channel information
    of a company.
    Each URL is considered as a channel in this
    architecture.
    """

    id = models.UUIDField(
        default=uuid.uuid4, verbose_name="Channel Id", primary_key=True, editable=True
    )
    type_name = models.ForeignKey(
        config_models.ChannelType, on_delete=models.CASCADE, related_name="type"
    )
    channel_name = models.CharField(
        verbose_name="Channel Name", max_length=50, null=True
    )
    company = models.ForeignKey(
        config_models.CompanyDetails, on_delete=models.CASCADE, null=True
    )
    url = models.URLField(
        verbose_name="Channel Url", unique=True, null=True, max_length=200
    )
    weightage = models.FloatField(verbose_name="Weightage", null=True, default=1.0)
    scores = models.OneToOneField(
        audit_models.ScoreCardParameter,
        on_delete=models.DO_NOTHING,
        related_name="channel",
        blank=True,
        null=True,
    )
    compliance_score = models.FloatField(verbose_name="Compliance Score", default=0)
    previous_compliance_score = models.FloatField(
        verbose_name="Previous Compliance Score", default=0
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.company} -> {self.url}"


class ChannelData(models.Model):
    """
    Table is used to store channel's data.
    Each channel i.e. URL can have multiple
    data entries in this table.
    """

    id = models.UUIDField(
        default=uuid.uuid4, verbose_name="Data Id", primary_key=True, editable=True
    )
    channel = models.ForeignKey("Channel", on_delete=models.CASCADE)
    scraped_data = models.TextField(verbose_name="Scarped Data", null=True)
    processed_data = models.TextField(
        verbose_name="Processed Data", null=True, blank=True
    )
    scores = models.OneToOneField(
        audit_models.ScoreCardParameter,
        on_delete=models.DO_NOTHING,
        related_name="channel_data",
        blank=True,
        null=True,
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.channel} data"
