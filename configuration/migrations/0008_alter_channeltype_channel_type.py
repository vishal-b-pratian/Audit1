# Generated by Django 4.1 on 2022-10-03 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configuration', '0007_engagement_client_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='channeltype',
            name='channel_type',
            field=models.CharField(max_length=50, verbose_name='Channel Type'),
        ),
    ]
