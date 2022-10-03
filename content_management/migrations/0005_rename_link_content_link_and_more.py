# Generated by Django 4.1 on 2022-10-02 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("content_management", "0004_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="content",
            old_name="Link",
            new_name="link",
        ),
        migrations.AlterField(
            model_name="unmappedkeywords",
            name="unmapped_keywords_count",
            field=models.IntegerField(null=True, verbose_name="Unmapped keyword count"),
        ),
    ]
