from django.db import models

# Create your models here.
from django.db import models
from django.utils.text import slugify
import uuid


class Homestay(models.Model):
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

    # Identity
    slug = models.SlugField(unique=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField()

    # Host (no auth for hackathon — plain fields)
    host_name = models.CharField(max_length=120)
    host_phone = models.CharField(max_length=40)
    host_email = models.EmailField(blank=True)

    # Location
    region = models.CharField(max_length=20, choices=REGION_CHOICES)
    address = models.CharField(max_length=300)
    latitude = models.FloatField()
    longitude = models.FloatField()

    # Property details
    price_per_night = models.DecimalField(max_digits=8, decimal_places=2)  # in INR
    max_guests = models.IntegerField(default=2)
    bedrooms = models.IntegerField(default=1)
    beds = models.IntegerField(default=1)
    bathrooms = models.IntegerField(default=1)

    amenities = models.JSONField(default=list, blank=True)
    # e.g. ["wifi", "kitchen", "parking", "hot_water", "meals_included"]

    images = models.JSONField(default=list, blank=True)  # URL list

    # Denormalized rating (fast reads)
    rating = models.FloatField(default=0.0)
    rating_count = models.IntegerField(default=0)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-rating", "-created_at"]
        indexes = [
            models.Index(fields=["region"]),
            models.Index(fields=["is_active"]),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title)[:180] or "homestay"
            self.slug = f"{base}-{uuid.uuid4().hex[:6]}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Booking(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("accepted", "Accepted"),
        ("declined", "Declined"),
        ("completed", "Completed"),
    ]

    homestay = models.ForeignKey(
        Homestay, on_delete=models.CASCADE, related_name="bookings"
    )

    # Tourist info (no auth — plain fields)
    guest_name = models.CharField(max_length=120)
    guest_phone = models.CharField(max_length=40)
    guest_email = models.EmailField(blank=True)

    check_in = models.DateField()
    check_out = models.DateField()
    guests = models.IntegerField(default=1)
    message = models.TextField(blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.guest_name} → {self.homestay.title}"


class Review(models.Model):
    homestay = models.ForeignKey(
        Homestay, on_delete=models.CASCADE, related_name="reviews"
    )
    author_name = models.CharField(max_length=120)
    rating = models.IntegerField()  # 1..5
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.author_name} → {self.rating}★"