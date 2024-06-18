from django.db import models
from app.models import UUIDTimestampedModel

class Document(UUIDTimestampedModel):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    blob_url = models.URLField()
    blob_metadata = models.JSONField(default=dict)

    def __str__(self):
        return f"{self.uuid} - {self.title}"
