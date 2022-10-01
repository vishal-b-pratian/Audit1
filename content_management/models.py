# from django.db import models
# from configuration import models as config_models
# import jsonfield


# class Content(models.Model):
#     channel = models.ForeignKey(to=config_models.Channel, on_delete = models.CASCADE)
#     title = models.TextField(null=False, verbose_name='Title', max_length=200,
#                              unique=True, default="Content Title")
#     number_of_words = models.IntegerField(verbose_name="Number Of Words", default=0)
#     main_content = models.TextField(verbose_name='Main Content', null=False)
#     created = models.DateTimeField(auto_now_add=True)
#     updated = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.title


# class ContentFetchInfo(models.Model):
#     channel = models.ForeignKey(to=config_models.Channel, on_delete = models.CASCADE)
#     date_time = models.DateTimeField(auto_now_add=True)
#     processed_words = models.TextField(verbose_name="Processed Words", null=False)
#     mapped_keywords_count = models.IntegerField(verbose_name="No. of Mapped Words", null=True)
#     unmapped_keywords_count = models.IntegerField(verbose_name="No. of Unmapped Words", null=True)

#     def __str__(self):
#         return self.processed_words

# class MappedKeyWords(models.Model):
#     channel = models.ForeignKey(to=config_models.Channel, on_delete = models.CASCADE)
#     mapped_keywords = jsonfield.JSONField()
#     # '{"DNA": {"a": 3, "b": 4, "c": 0}, "Differentiator": {"g": 5, "h": 2}}'

#     # MA - ['dna': ['a', 'b', 'd']]
#     def __str__(self):
#         return str(self.channel.channel_name)


# class UnmappedKeywords(models.Model):
#     channel = models.ForeignKey(to=config_models.Channel, on_delete = models.CASCADE)
#     unmapped_keywords = models.TextField(verbose_name="Unmapped Keywords", null=True)

#     def __str__(self):
#         return self.unmapped_keywords
