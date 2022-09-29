from django.contrib import admin
from . import models as audit_models

# Register your models here.
admin.site.register(audit_models.AuditInformation)
admin.site.register(audit_models.ChannelParameterScore)
admin.site.register(audit_models.SourceParameterScore)
admin.site.register(audit_models.ChannelTypeParameterScore)
