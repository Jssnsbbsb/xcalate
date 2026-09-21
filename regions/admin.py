from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Region


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "latitude", "longitude", "size_mb")
    prepopulated_fields = {"slug": ("name",)}