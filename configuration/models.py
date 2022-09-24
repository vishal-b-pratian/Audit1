import uuid
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

# Create your models here.
class CompanyDetails(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, verbose_name="Company Id", primary_key=True, editable=True
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="company")
    name = models.CharField(verbose_name="Company Name", null=True, max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(verbose_name="Is Active", default=True)

    def __str__(self):
        return self.name


class MessageArchitecture(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, verbose_name="MA Id", primary_key=True, editable=True
    )
    company = models.OneToOneField("CompanyDetails", on_delete=models.CASCADE)

    def __str__(self):
        return f"MA for {self.company}"


class Measures(models.Model):
    class FieldChoices(models.TextChoices):
        DNA = "dna", _("DNA")
        POSMO_TAG = "posmotag", _("POSMO TAG")
        DIFFERENTIATOR = "differentiator", _("Differentiator")
        VALUE_PROPOSITION = "value proposition", _("Value Proposition")
        TAGLINE = "tagline", _("Tagline")

    # class Meta:
    #     unique_together = [["message_architecture", "field_name"]]

    id = models.UUIDField(
        default=uuid.uuid4, verbose_name="Measure Id", primary_key=True, editable=True
    )
    message_architecture = models.ForeignKey(
        "MessageArchitecture", on_delete=models.CASCADE, related_name="measure_field"
    )
    field_name = models.CharField(
        verbose_name="Field Name", choices=FieldChoices.choices, max_length=30
    )
    value = models.TextField(verbose_name="Value", max_length=1000, null=True)
    # ^^^ How to store the keywords? Right now it is stored as space separated string.
    weightage = models.FloatField(verbose_name="Weightage", null=True, default=1.0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.message_architecture} -> {self.field_name}"


class ChannelType(models.Model):
    type_name = models.CharField(
        max_length=50, unique=True, verbose_name="Channel Type"
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(verbose_name="Is Active", default=True)

    def __str__(self):
        return self.type_name


class ChannelTypeWeightage(models.Model):
    company = models.ForeignKey(
        "CompanyDetails", on_delete=models.CASCADE, related_name="company"
    )
    channel_type = models.ForeignKey(
        "ChannelType", on_delete=models.CASCADE, related_name="channel_type"
    )
    weightage = models.FloatField(verbose_name="Weightage", null=True, default=1.0)

    def __str__(self):
        return f"{self.company} -> {self.channel_type}"


class Channel(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, verbose_name="Channel Id", primary_key=True, editable=True
    )
    type_name = models.ForeignKey(
        "ChannelType", on_delete=models.CASCADE, related_name="type"
    )
    company = models.ForeignKey("CompanyDetails", on_delete=models.CASCADE, null=True)
    url = models.URLField(
        verbose_name="Channel Url", unique=True, null=True, max_length=200
    )
    weightage = models.FloatField(verbose_name="Weightage", null=True, default=1.0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

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


class ScoreCard(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, verbose_name="Score Id", primary_key=True, editable=True
    )
    content = models.ForeignKey("ChannelData", on_delete=models.CASCADE)
    dna_alignment = models.FloatField(verbose_name="DNA Alignment", default=0.0)
    posmo_tag = models.FloatField(verbose_name="Posmo Tag", default=0.0)
    differentiator = models.FloatField(verbose_name="Differentiator", default=0.0)
    value_proposition = models.FloatField(verbose_name="Value Proposition", default=0.0)
    tagline = models.FloatField(verbose_name="Tagline", default=0.0)
    total_score = models.FloatField(verbose_name="Total Score", default=0.0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.content} score card"
