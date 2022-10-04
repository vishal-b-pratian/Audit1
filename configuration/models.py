import uuid
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


# This variable stores the audit types, used as choices in :model: 'models.Engagement 
PREDEFINED_AUDIT_TYPES = (
    ("branding", "branding"),
    ("positioning", "positioning"),
    ("both", "both")
)


class CompanyDetails(models.Model):
    """
    Stores a single company details, related to :model:'auth.User'.
    """

    id = models.UUIDField(
        default=uuid.uuid4, verbose_name="Company Id", primary_key=True, editable=True
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="company")
    name = models.CharField(verbose_name="Company Name", null=True, max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(verbose_name="Is Active", default=True)
    compliance_score = models.FloatField(verbose_name="Present Compliance Score", default=0)
    previous_compliance_score = models.FloatField(
        verbose_name="Previous Compliance Score", default=-1
    )

    def __str__(self):
        return self.name


class ClientType(models.Model):
    """
    Stores the type of the company. i.e., Specifies whether the company is serving in health or education etc.
    """

    id = models.UUIDField(default=uuid.uuid4, verbose_name="Id", primary_key=True)
    name = models.CharField(max_length=50, unique=True)  # ensure case is handled propery to make Client Type unique

    def __str__(self):
        return self.name


class Engagement(models.Model):
    """
    Stores the type of engagement(audit), related to :model: 'models.CompanyDetails' and  :model: 'models.ClientType'.
    """

    class Meta:
        unique_together = [['type', 'company']]

    id = models.UUIDField(
        default=uuid.uuid4, 
        verbose_name="Engagement_Id", 
        primary_key=True, 
        editable=True
    )
    name = models.CharField(max_length=100, default='')
    client_type = models.ForeignKey(to="ClientType", on_delete=models.PROTECT,)
    company = models.ForeignKey("CompanyDetails", on_delete=models.CASCADE)
    start_Date = models.DateField(auto_now_add=True, verbose_name="Start Date")
    end_Date = models.DateField()
    is_active = models.BooleanField(verbose_name="Is Active", default=True)
    type = models.CharField(
        max_length=70,
        choices=PREDEFINED_AUDIT_TYPES)
    compliance_score = models.FloatField(verbose_name="Present Compliance Score", default=0)
    previous_compliance_score = models.FloatField(verbose_name="Previous Compliance Score", default=-1)

    def __str__(self):
        return f"{self.company.name} - {self.type}"


class MessageArchitecture(models.Model):
    """
    Stores the message architecture of the company audit.
    Related to :model: 'models.Engagement'
    """

    id = models.UUIDField(
        default=uuid.uuid4, verbose_name="MA Id", primary_key=True, editable=True
    )
    engagement = models.ForeignKey(to="Engagement", on_delete=models.CASCADE)
    parameter = models.CharField(verbose_name="Parameter Name", max_length=200)
    keyword = models.CharField(verbose_name="Keyword", max_length=200)

    def __str__(self):
        return f"MA for {self.company}"


class AuditParameter(models.Model):
    """
    Stores the details such as, parameter, keyword, contents
    related to the engagement(audit).
    Related to :model: 'models.Engagement'
    """

    id = models.UUIDField(
        default=uuid.uuid4,
        verbose_name="Audit Parameter Id",
        primary_key=True,
        editable=True
    )
    engagement = models.ForeignKey(
        to="Engagement",
        verbose_name="Engagement Details",
        on_delete=models.DO_NOTHING
    )
    parameter = models.CharField(verbose_name="Parameter Name", max_length=200)
    audit_weightage = models.FloatField(
        verbose_name="Audit Weightage",
        null=True,
        default=1.0
    )
    keyword = models.CharField(
        verbose_name="Keyword",
        max_length=200
    )
    parameter_content = models.TextField(null=True)

    def __str__(self) -> str:
        return f"{self.parameter}"


class ChannelType(models.Model):
    """
    Stores the basic details for the channel type.
    Related to :model: 'models.Engagement'
    """

    class Meta:
        unique_together = [['channel_type', 'engagement']]

    id = models.UUIDField(
        default=uuid.uuid4,
        verbose_name="Channel Type Id",
        primary_key=True,
        editable=True
    )
    channel_type = models.CharField(
        max_length=50,
        verbose_name="Channel Type",
    )
    engagement = models.ForeignKey(
        to="Engagement",
        on_delete=models.CASCADE,
        related_name="engagement_details",
    )
    channel_type_weightage = models.FloatField(
        verbose_name="Weightage",
        null=True,
        default=1.0
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(
        verbose_name="Is Active",
        default=True
    )

    def __str__(self):
        return f"{self.engagement.company.name} - {self.channel_type}"


class ChannelTypeParameter(models.Model):
    """
    Stores the weights and parameters for each channel type.
    Related to :model: 'models.ChannelType' and :model: 'models.AuditParameter'.
    """

    class Meta:
        unique_together = [['type_name', 'parameters']]

    type_name = models.ForeignKey(
        to="ChannelType",
        on_delete=models.CASCADE
    )
    parameters = models.ForeignKey(
        to="AuditParameter",
        on_delete=models.DO_NOTHING
    )
    weight = models.FloatField()

    def __str__(self):
        return f'{self.parameters} | {self.weight} | {self.type_name}'


class ChannelName(models.Model):
    """
    Stores the channel name based on the table :model: 'models.ChannelType'
    """

    class Meta:
        unique_together = [['channel_type_name', 'channel_name']]

    channel_type_name = models.ForeignKey(
        to="ChannelType",
        on_delete=models.DO_NOTHING)
    channel_name = models.CharField(
        verbose_name="Channel Name",
        max_length=70
    )

    def __str__(self):
        return f" {self.channel_name}"


class ChannelParameter(models.Model):
    """
    Stores the parameter and weights for an entry of channel.
    Related to :model: 'models.Channels'
    """

    class Meta:
        unique_together = [['channel', 'parameters']]

    channel = models.ForeignKey(
        to="Channel", on_delete=models.CASCADE, related_name="channel"
    )
    parameters = models.ForeignKey(
        to="AuditParameter",
        on_delete=models.DO_NOTHING
    )
    weight = models.FloatField()

    def __str__(self):
        return f'{self.parameters} | {self.weight} | {self.channel}'


class Channel(models.Model):
    """
    Stores all the details of the channel including the links.
    Related to :model: 'models.ChannelName', :model: 'models.ChannelType' and :model: 'models.Engagement'
    """

    id = models.UUIDField(
        default=uuid.uuid4,
        verbose_name="Channel Id",
        primary_key=True,
        editable=True
    )
    channel_title = models.CharField(
        verbose_name="channel_Title",
        null=True,
        max_length=200
    )
    channel_name = models.ForeignKey(
        to="ChannelName",
        on_delete=models.CASCADE,
    )
    type_name = models.ForeignKey(
        to="ChannelType",
        on_delete=models.CASCADE,
    )
    engagement = models.ForeignKey(
        to="Engagement",
        on_delete=models.DO_NOTHING,
    )
    url = models.URLField(
        verbose_name="Channel Url", 
        max_length=200,
        null=True
    )
    compliance_score = models.FloatField(verbose_name="Present Compliance Score", default=0)
    previous_compliance_score = models.FloatField(verbose_name="Previous Compliance Score", default=-1)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f" {self.url}"


class ChannelSourceParameter(models.Model):
    """
    Stores the paramters and weights with respect to a single entry of channel source.
    Related to :model: 'models.Channel'
    """

    class Meta:
        unique_together = [['channel', 'parameters']]

    channel = models.ForeignKey(
        to="Channel",
        verbose_name="Channel Url",
        max_length=200,
        on_delete=models.DO_NOTHING
    )
    parameters = models.ForeignKey(
        to="AuditParameter",
        on_delete=models.DO_NOTHING
    )
    weight = models.FloatField()

    def __str__(self):
        return f'{self.parameters} | {self.weight} | {self.channel}'