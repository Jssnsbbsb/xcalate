from rest_framework import serializers
from .models import Region


class RegionListSerializer(serializers.ModelSerializer):
    place_count = serializers.SerializerMethodField()

    class Meta:
        model = Region
        fields = [
            "id", "slug", "name", "description", "cover_image",
            "latitude", "longitude", "zoom", "size_mb", "place_count",
        ]

    def get_place_count(self, obj):
        from places.models import Place
        return Place.objects.filter(region=obj.slug).count()


class RegionDetailSerializer(RegionListSerializer):
    class Meta(RegionListSerializer.Meta):
        fields = RegionListSerializer.Meta.fields