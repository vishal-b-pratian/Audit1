# Generated by Django 4.1.1 on 2022-09-27 17:10

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("audit_engine", "0001_initial"),
        ("configuration", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Channel",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        primary_key=True,
                        serialize=False,
                        verbose_name="Channel Id",
                    ),
                ),
                (
                    "channel_name",
                    models.CharField(
                        max_length=50, null=True, verbose_name="Channel Name"
                    ),
                ),
                (
                    "url",
                    models.URLField(null=True, unique=True, verbose_name="Channel Url"),
                ),
                (
                    "weightage",
                    models.FloatField(default=1.0, null=True, verbose_name="Weightage"),
                ),
                (
                    "compliance_score",
                    models.FloatField(default=0, verbose_name="Compliance Score"),
                ),
                (
                    "previous_compliance_score",
                    models.FloatField(
                        default=0, verbose_name="Previous Compliance Score"
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                (
                    "company",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="configuration.companydetails",
                    ),
                ),
                (
                    "scores",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="channel",
                        to="audit_engine.scorecardparameter",
                    ),
                ),
                (
                    "type_name",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="type",
                        to="configuration.channeltype",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ChannelData",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        primary_key=True,
                        serialize=False,
                        verbose_name="Data Id",
                    ),
                ),
                (
                    "scraped_data",
                    models.TextField(null=True, verbose_name="Scarped Data"),
                ),
                (
                    "processed_data",
                    models.TextField(
                        blank=True, null=True, verbose_name="Processed Data"
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                (
                    "channel",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="content_management.channel",
                    ),
                ),
                (
                    "scores",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="channel_data",
                        to="audit_engine.scorecardparameter",
                    ),
                ),
            ],
        ),
    ]
