import uuid
from django.db import models
from django.contrib.auth.models import User
from content_management import models as content_models
from configuration import models as config_models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class AuditInformation(models.Model):
    channel_name = models.ForeignKey(
        config_models.ChannelName,
        on_delete=models.CASCADE,
        related_name="audit_info",
    )
    start_date = models.DateField(verbose_name="Start Date")
    end_date = models.DateField(verbose_name="End Date")
    overall_compliance_score = models.FloatField(
        verbose_name="Overall Compliance Score",
        default=0.0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Audit info <{self.channel_name}>"


class SourceParameterScore(models.Model):
    scource = models.ForeignKey(
        config_models.ChannelSourceParameter, on_delete=models.CASCADE, related_name="parameter"
    )
    id = models.UUIDField(
        default=uuid.uuid4,
        verbose_name="Source Parameter Id",
        primary_key=True,
        editable=True,
    )
    parametersScores = models.CharField(verbose_name="Source Parameters", max_length=2000)


class ChannelParameterScore(models.Model):
    channel = models.ForeignKey(
        config_models.ChannelParameter, on_delete=models.CASCADE, related_name="parameter"
    )
    id = models.UUIDField(
        default=uuid.uuid4,
        verbose_name="Channel Parameter Id",
        primary_key=True,
        editable=True,
    )
    parameters = models.CharField(verbose_name="Channel Parameters", max_length=2000)


class ChannelTypeParameterScore(models.Model):
    channel_type = models.ForeignKey(
        config_models.ChannelTypeParameter, on_delete=models.CASCADE, related_name="parameter"
    )
    id = models.UUIDField(
        default=uuid.uuid4,
        verbose_name="ChannelType Parameter Id",
        primary_key=True,
        editable=True,
    )
    parameters = models.CharField(
        verbose_name="ChannelType Parameters", max_length=2000
    )

# class ScoreCardParameter(models.Model):
#     """
#     Table is used to store scores for each
#     parameter.
#     """

#     id = models.UUIDField(
#         default=uuid.uuid4, verbose_name="Score Id", primary_key=True, editable=True
#     )
#     dna_alignment = models.FloatField(verbose_name="DNA Alignment", default=0.0)
#     posmo_tag = models.FloatField(verbose_name="Posmo Tag", default=0.0)
#     differentiator = models.FloatField(verbose_name="Differentiator", default=0.0)
#     value_proposition = models.FloatField(verbose_name="Value Proposition", default=0.0)
#     tagline = models.FloatField(verbose_name="Tagline", default=0.0)
#     total_score = models.FloatField(verbose_name="Total Score", default=0.0)
#     created = models.DateTimeField(auto_now_add=True)
#     updated = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"{self.id}"
