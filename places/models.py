
# Create your models here.
from django.db import models


class Place(models.Model):
    CATEGORY_CHOICES = [
        ("monument", "Monument"),
        ("nature", "Nature"),
        ("restaurant", "Restaurant"),
        ("heritage", "Heritage"),
        ("temple", "Temple"),
        ("market", "Market"),
        ("adventure", "Adventure"),
    ]

    REGION_CHOICES = [
        ("imphal", "Imphal"),
        ("loktak", "Loktak"),
        ("ukhrul", "Ukhrul"),
        ("churachandpur", "Churachandpur"),
        ("senapati", "Senapati"),
        ("tamenglong", "Tamenglong"),
        ("bishnupur", "Bishnupur"),
        ("thoubal", "Thoubal"),
    ]

    # Core
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    region = models.CharField(max_length=20, choices=REGION_CHOICES)

    # Content
    short_description = models.CharField(max_length=280)
    description = models.TextField(blank=True)
    images = models.JSONField(default=list, blank=True)   # list of URLs

    # Location
    latitude = models.FloatField()
    longitude = models.FloatField()
    address = models.CharField(max_length=300, blank=True)

    # Meta
    rating = models.FloatField(default=0.0)
    rating_count = models.IntegerField(default=0)
    price_range = models.CharField(max_length=20, blank=True)   # "budget", "mid", "premium"
    tags = models.JSONField(default=list, blank=True)           # ["lake", "sunset", "boating"]
    opening_hours = models.CharField(max_length=120, blank=True)
    contact = models.CharField(max_length=60, blank=True)

    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-is_featured", "-rating", "name"]
        indexes = [
            models.Index(fields=["category"]),
            models.Index(fields=["region"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.category})"