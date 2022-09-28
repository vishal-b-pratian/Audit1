import uuid
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

# Create your models here.
class CompanyDetails(models.Model):
    """
    Table to store company details.
    """

    id = models.UUIDField(
        default=uuid.uuid4, verbose_name="Company Id", primary_key=True, editable=True
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="company")
    name = models.CharField(verbose_name="Company Name", null=True, max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(verbose_name="Is Active", default=True)
    compliance_score = models.FloatField(verbose_name="Compliance Score", default=0)
    previous_compliance_score = models.FloatField(
        verbose_name="Compliance Score", default=0
    )

    def __str__(self):
        return self.name


class DNAElement(models.Model):
    dna_type = models.CharField(verbose_name="DNA Type", max_length=10, null=True)
    keywords = models.TextField(verbose_name="Keywords", null=True)
    # ^^^ How to store the keywords? Right now it is stored as space separated string.

    def __str__(self):
        return self.dna_type


class MessageArchitecture(models.Model):
    """
    Table is used to eastablish a relationship
    between company and its MA parameters.
    """

    id = models.UUIDField(
        default=uuid.uuid4, verbose_name="MA Id", primary_key=True, editable=True
    )
    company = models.OneToOneField("CompanyDetails", on_delete=models.CASCADE)

    def __str__(self):
        return f"MA for {self.company}"


class ParameterType(models.Model):
    """
    Table to store different parameter names
    of a MA such as dna, differentiator etc.

    It is only accessed by the admin team.
    """

    parameter_name = models.CharField(
        verbose_name="Parameter Name", max_length=20, null=True
    )

    def __str__(self):
        return self.parameter_name


# class FieldChoices(models.TextChoices):
#     DNA = "dna", _("DNA")
#     POSMO_TAG = "posmotag", _("POSMO TAG")
#     DIFFERENTIATOR = "differentiator", _("Differentiator")
#     VALUE_PROPOSITION = "value proposition", _("Value Proposition")
#     TAGLINE = "tagline", _("Tagline")


class Measure(models.Model):
    """
    Table to store parameters of a MA
    which different keywords in different
    rows.
    """

    id = models.UUIDField(
        default=uuid.uuid4, verbose_name="Measure Id", primary_key=True, editable=True
    )
    message_architecture = models.ForeignKey(
        "MessageArchitecture", on_delete=models.CASCADE, related_name="measure_field"
    )
    parameter = models.ForeignKey("ParameterType", on_delete=models.CASCADE)
    value = models.TextField(verbose_name="Value", max_length=1000, null=True)
    # ^^^ How to store the keywords? Right now it is stored as space separated string.
    weightage = models.FloatField(verbose_name="Weightage", null=True, default=1.0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.message_architecture} -> {self.parameter}"


class ChannelType(models.Model):
    """
    Table to store different channel types
    such as social media, news website, and
    company webiste.
    """

    type_name = models.CharField(
        max_length=50, unique=True, verbose_name="Channel Type"
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(verbose_name="Is Active", default=True)

    def __str__(self):
        return self.type_name


class ChannelTypeWeightage(models.Model):
    """
    Enables to store different weights for each channel
    type for different users.
    """

    class Meta:
        unique_together = [["company", "channel_type"]]

    company = models.ForeignKey(
        "CompanyDetails",
        on_delete=models.CASCADE,
        related_name="channel_type_weightage",
    )
    channel_type = models.ForeignKey(
        "ChannelType", on_delete=models.CASCADE, related_name="channel_type"
    )
    weightage = models.FloatField(verbose_name="Weightage", null=True, default=1.0)

    def __str__(self):
        return f"{self.company} -> {self.channel_type}"
