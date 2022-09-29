# Generated by Django 3.2 on 2022-09-29 12:23

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Content',
            fields=[
                ('channel_id', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('title', models.TextField(default='Content Title', max_length=200, unique=True, verbose_name='Title')),
                ('number_of_words', models.IntegerField(default=0, verbose_name='Number Of Words')),
                ('main_content', models.TextField(verbose_name='Main Content')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='ContentFetchInfo',
            fields=[
                ('channel_id', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('date_time', models.DateTimeField(auto_now_add=True)),
                ('processed_words', models.TextField(verbose_name='Processed Words')),
                ('mapped_keywords_count', models.IntegerField(null=True, verbose_name='No. of Mapped Words')),
                ('unmapped_keywords_count', models.IntegerField(null=True, verbose_name='No. of Unmapped Words')),
            ],
        ),
        migrations.CreateModel(
            name='Links',
            fields=[
                ('channel_id', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('url', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='MappedKeyWords',
            fields=[
                ('channel_id', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('mapped_keywords', jsonfield.fields.JSONField(default=dict)),
            ],
        ),
        migrations.CreateModel(
            name='UnmappedKeywords',
            fields=[
                ('channel_id', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('unmapped_keywords', models.TextField(null=True, verbose_name='Unmapped Keywords')),
            ],
        ),
    ]
