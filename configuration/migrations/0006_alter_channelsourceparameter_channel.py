# Generated by Django 3.2 on 2022-10-01 02:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('configuration', '0005_auto_20221001_0000'),
    ]

    operations = [
        migrations.AlterField(
            model_name='channelsourceparameter',
            name='channel',
            field=models.ForeignKey(max_length=200, on_delete=django.db.models.deletion.CASCADE, to='configuration.channel', verbose_name='Channel'),
        ),
    ]
