# Generated by Django 4.1 on 2022-10-02 04:59

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("configuration", "0007_auto_20221001_1543"),
    ]

    operations = [
        migrations.CreateModel(
            name="ClientType",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        primary_key=True,
                        serialize=False,
                        verbose_name="Id",
                    ),
                ),
                ("name", models.CharField(max_length=50)),
            ],
        ),
    ]
