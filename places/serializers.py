from rest_framework import serializers
from .models import Place


class PlaceListSerializer(serializers.ModelSerializer):
    """Compact — for lists, carousels, map pins."""
    class Meta:
        model = Place
        fields = [
            "id", "name", "slug", "category", "region",
            "short_description", "images", "latitude", "longitude",
            "rating", "rating_count", "price_range", "tags", "is_featured",
        ]


class PlaceDetailSerializer(serializers.ModelSerializer):
    """Full — for detail page."""
    class Meta:
        model = Place
        fields = "__all__"