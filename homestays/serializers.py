from rest_framework import serializers
from users.models import User

from .models import Homestay, Booking, Review


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["id", "author_name", "rating", "comment", "created_at"]


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = [
            "id", "guest_name", "guest_phone", "guest_email",
            "check_in", "check_out", "guests", "message",
            "status", "created_at",
        ]
        read_only_fields = ["id", "status", "created_at"]

    def validate(self, data):
        if data["check_in"] >= data["check_out"]:
            raise serializers.ValidationError("check_out must be after check_in")
        if data["guests"] < 1:
            raise serializers.ValidationError("guests must be at least 1")
        return data


class HomestayListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Homestay
        fields = [
            "id", "slug", "title", "region", "price_per_night",
            "max_guests", "bedrooms", "beds", "bathrooms",
            "amenities", "images", "rating", "rating_count",
            "latitude", "longitude",
        ]


class HomestayHostSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "phone", "business_name"]
        read_only_fields = fields


class HomestayDetailSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    host = HomestayHostSerializer(source="user", read_only=True)

    class Meta:
        model = Homestay
        fields = "__all__"


class HomestayCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Homestay
        fields = [
            "title", "description",
            "region", "address", "latitude", "longitude",
            "price_per_night", "max_guests", "bedrooms", "beds", "bathrooms",
            "amenities", "images",
        ]

    def validate_images(self, value):
        if not isinstance(value, list):
            raise serializers.ValidationError("images must be a list of URLs")
        if len(value) > 15:
            raise serializers.ValidationError("max 15 images")
        return value

    def validate_amenities(self, value):
        if not isinstance(value, list):
            raise serializers.ValidationError("amenities must be a list")
        return value