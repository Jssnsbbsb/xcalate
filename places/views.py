from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import Place
from .serializers import PlaceListSerializer, PlaceDetailSerializer


@api_view(["GET"])
def place_list(request):
    """
    GET /api/places/
    Query params:
      - category=monument
      - region=imphal
      - featured=true
      - search=lake
      - limit=20
    """
    qs = Place.objects.all()

    category = request.query_params.get("category")
    region = request.query_params.get("region")
    featured = request.query_params.get("featured")
    search = request.query_params.get("search")

    if category:
        qs = qs.filter(category=category)
    if region:
        qs = qs.filter(region=region)
    if featured and featured.lower() == "true":
        qs = qs.filter(is_featured=True)
    if search:
        qs = qs.filter(name__icontains=search) | qs.filter(short_description__icontains=search)

    try:
        limit = min(int(request.query_params.get("limit", 50)), 200)
    except ValueError:
        limit = 50

    qs = qs[:limit]
    serializer = PlaceListSerializer(qs, many=True)
    return Response({
        "count": len(serializer.data),
        "results": serializer.data,
    })


@api_view(["GET"])
def place_detail(request, slug):
    """
    GET /api/places/<slug>/
    """
    place = get_object_or_404(Place, slug=slug)
    return Response(PlaceDetailSerializer(place).data)


@api_view(["GET"])
def place_categories(request):
    """GET /api/places/categories/ — for filter UI."""
    return Response({
        "categories": [
            {"id": c[0], "label": c[1]} for c in Place.CATEGORY_CHOICES
        ]
    })