from django.db import models

# Create your models here.

from pgvector.django import VectorField

from app.models import UUIDTimestampedModel


class ImageDocument(UUIDTimestampedModel):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to="images/", blank=True, null=True)
    blob_metadata = models.JSONField(default=dict)
    image_embedding = VectorField(dimensions=512, null=True)

    def __str__(self):
        return f"{self.uuid} - {self.title} - {self.caption}"
