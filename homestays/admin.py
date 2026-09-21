from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Homestay, Booking, Review


class BookingInline(admin.TabularInline):
    model = Booking
    extra = 0


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0


@admin.register(Homestay)
class HomestayAdmin(admin.ModelAdmin):
    list_display = ("title", "region", "host_name", "price_per_night", "rating", "is_active")
    list_filter = ("region", "is_active")
    search_fields = ("title", "host_name", "address")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [BookingInline, ReviewInline]


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("guest_name", "homestay", "check_in", "check_out", "status", "created_at")
    list_filter = ("status",)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("author_name", "homestay", "rating", "created_at")
    list_filter = ("rating",)