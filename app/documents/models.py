from django.db import models
from pgvector.django import VectorField

from app.models import UUIDTimestampedModel


class Document(UUIDTimestampedModel):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    # using this later with CLIP / Image search / keeping the raw blob
    blob_url = models.URLField()
    blob_metadata = models.JSONField(default=dict)
    text_embedding = VectorField(dimensions=512, null=True)  # should use separate collection but we're good for now

    def __str__(self):
        return f"{self.uuid} - {self.title}"
