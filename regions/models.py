from django.db import models

# Create your models here.
from django.db import models


class Region(models.Model):
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    cover_image = models.URLField(blank=True)

    # Map defaults
    latitude = models.FloatField()
    longitude = models.FloatField()
    zoom = models.IntegerField(default=11)

    # Offline metadata
    size_mb = models.FloatField(default=0.0)   # approx download size

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name