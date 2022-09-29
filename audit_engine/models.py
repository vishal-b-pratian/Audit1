import uuid
from django.db import models
from configuration import models as config_models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.


class AuditInformation(models.Model):
    company = models.ForeignKey(
        config_models.CompanyDetails,
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
        return f"Audit info <{self.company}>"


class SourceParameterScore(models.Model):
    scource = models.ForeignKey(
        config_models.ChannelSource, on_delete=models.CASCADE, related_name="parameter"
    )
    id = models.UUIDField(
        default=uuid.uuid4,
        verbose_name="Source Parameter Id",
        primary_key=True,
        editable=True,
    )
    parameters = models.CharField(verbose_name="Source Parameters", max_length=2000)


class ChannelParameterScore(models.Model):
    channel = models.ForeignKey(
        config_models.Channel, on_delete=models.CASCADE, related_name="parameter"
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
        config_models.ChannelType, on_delete=models.CASCADE, related_name="parameter"
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
