from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.CompanyDetails)
admin.site.register(models.ChannelType)
admin.site.register(models.ChannelTypeWeightage)
admin.site.register(models.Channel)
admin.site.register(models.ChannelData)
admin.site.register(models.ScoreCard)
admin.site.register(models.MessageArchitecture)
admin.site.register(models.Measures)
