from . import models
from django.contrib import admin
from content_management import models as content_models

# Register your models here.
admin.site.register(content_models.Links)
admin.site.register(content_models.Content)
admin.site.register(content_models.ContentFetchInfo)
admin.site.register(content_models.MappedKeyWords)
admin.site.register(content_models.UnmappedKeywords)
