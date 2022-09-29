import uuid
from email.policy import default
from tabnanny import verbose
from django.db import models
import jsonfield


class Links(models.Model):
    channel_id = models.CharField(max_length = 30, primary_key = True)
    url = models.URLField()

class Content(models.Model):
    #id = models.CharField()
    channel_id = models.CharField(max_length = 30, primary_key = True)
    title=models.TextField(null=False,verbose_name='Title',max_length = 200,  
                    unique = True,default="Content Title")
    number_of_words=models.IntegerField(verbose_name="Number Of Words",default=0)
    main_content=models.TextField(verbose_name='Main Content',null= False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):

        return self.title


class ContentFetchInfo(models.Model):
    channel_id = models.CharField(max_length = 30, primary_key = True)
    date_time = models.DateTimeField(auto_now_add = True)
    processed_words = models.TextField(verbose_name = "Processed Words", null = False)
    mapped_keywords_count = models.IntegerField(verbose_name = "No. of Mapped Words", null = True)
    unmapped_keywords_count = models.IntegerField(verbose_name = "No. of Unmapped Words", null = True)

    def __str__(self):

        return self.processed_words


class MappedKeyWords(models.Model):
    channel_id = models.CharField(max_length = 30, primary_key = True)
    mapped_keywords = jsonfield.JSONField()

    def __str__(self):

        return self.mapped_keywords


class UnmappedKeywords(models.Model):
    channel_id = models.CharField(max_length = 30, primary_key = True)
    unmapped_keywords=models.TextField(verbose_name="Unmapped Keywords",null=True)

     
    def __str__ (self):

        return self.unmapped_keywords