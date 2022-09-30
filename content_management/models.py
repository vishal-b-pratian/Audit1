import uuid
from django.db import models
from configuration import models as config_models

# Create your models here.

class ChannelData(models.Model):
    """
    Table is used to store channel's data.
    Each channel i.e. URL can have multiple
    data entries in this table.
    """

    id = models.UUIDField(
        default=uuid.uuid4, verbose_name="Data Id", primary_key=True, editable=True
    )
    channel = models.ForeignKey(config_models.Channel, on_delete=models.CASCADE)
    scraped_data = models.TextField(verbose_name="Scarped Data", null=True)
    processed_data = models.TextField(
        verbose_name="Processed Data", null=True, blank=True
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.channel} data"
