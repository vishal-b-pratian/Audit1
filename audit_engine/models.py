import uuid
from django.db import models
from content_management import models as content_models

# Create your models here.


class ScoreCard(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, verbose_name="Score Id", primary_key=True, editable=True
    )
    content = models.ForeignKey(content_models.ChannelData, on_delete=models.CASCADE)
    dna_alignment = models.FloatField(verbose_name="DNA Alignment", default=0.0)
    posmo_tag = models.FloatField(verbose_name="Posmo Tag", default=0.0)
    differentiator = models.FloatField(verbose_name="Differentiator", default=0.0)
    value_proposition = models.FloatField(verbose_name="Value Proposition", default=0.0)
    tagline = models.FloatField(verbose_name="Tagline", default=0.0)
    total_score = models.FloatField(verbose_name="Total Score", default=0.0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.content} score card"
