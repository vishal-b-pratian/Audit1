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
