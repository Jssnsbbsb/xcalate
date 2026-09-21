from datetime import datetime, timezone

from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Region
from .serializers import RegionListSerializer

from places.models import Place
from places.serializers import PlaceListSerializer

from homestays.models import Homestay
from homestays.serializers import HomestayListSerializer


@api_view(["GET"])
def region_list(request):
    """
    GET /api/regions/
    List all regions with their place counts.
    """
    qs = Region.objects.all()
    return Response({
        "count": qs.count(),
        "results": RegionListSerializer(qs, many=True).data,
    })


@api_view(["GET"])
def region_detail(request, slug):
    """
    GET /api/regions/<slug>/
    Lightweight metadata + has_places flag.
    Use /download/ for the full offline bundle.
    """
    region = get_object_or_404(Region, slug=slug)

    data = RegionListSerializer(region).data
    data["has_places"] = Place.objects.filter(region=slug).exists()
    data["has_homestays"] = Homestay.objects.filter(region=slug, is_active=True).exists()

    return Response(data)


@api_view(["GET"])
def region_download(request, slug):
    """
    GET /api/regions/<slug>/download/
    ⭐ The full offline bundle for the PWA to cache in IndexedDB.
    Includes: region metadata, all places, all active homestays, artists (TODO).
    """
    region = get_object_or_404(Region, slug=slug)

    places = Place.objects.filter(region=slug)
    homestays = Homestay.objects.filter(region=slug, is_active=True)

    return Response({
        "region": RegionListSerializer(region).data,
        "places": PlaceListSerializer(places, many=True).data,
        "homestays": HomestayListSerializer(homestays, many=True).data,
        "artists": [],  # TODO: fill once artists app exists
        "version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    })