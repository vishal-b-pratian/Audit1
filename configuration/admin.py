from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.CompanyDetails)
admin.site.register(models.ChannelType)
admin.site.register(models.DNAElement)
admin.site.register(models.ParameterType)
admin.site.register(models.ChannelTypeWeightage)
admin.site.register(models.MessageArchitecture)
admin.site.register(models.Measure)
admin.site.register(models.Channel)
admin.site.register(models.ChannelSource)
admin.site.register(models.ChannelParameterWeights)
admin.site.register(models.ChannelTypeParameterWeights)
admin.site.register(models.ChannelSourceParameterWeights)
admin.site.register(models.Engagement)
admin.site.register(models.EngagementType)
