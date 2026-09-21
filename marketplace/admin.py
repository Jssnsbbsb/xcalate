from django.contrib import admin

from .models import Listing


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
	list_display = (
		"title",
		"user",
		"type",
		"category",
		"region",
		"price",
		"is_active",
		"is_featured",
		"created_at",
	)
	list_filter = ("type", "category", "region", "is_active", "is_featured")
	search_fields = ("title", "description", "short_description", "user__username")
	prepopulated_fields = {"slug": ("title",)}
