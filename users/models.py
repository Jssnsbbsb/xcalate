from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        TOURIST = "tourist", "Tourist"
        LOCAL = "local", "Local"
        ADMIN = "admin", "Admin"

    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.TOURIST,
    )
    phone = models.CharField(max_length=40, blank=True)
    region = models.CharField(max_length=40, blank=True)
    bio = models.TextField(blank=True)
    avatar_url = models.URLField(blank=True)
    business_name = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.username
