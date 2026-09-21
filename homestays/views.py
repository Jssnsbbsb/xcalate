from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status

from .models import Homestay, Booking, Review
from .serializers import (
    HomestayListSerializer,
    HomestayDetailSerializer,
    HomestayCreateSerializer,
    BookingSerializer,
    ReviewSerializer,
)


# ---------- Listings ----------

@api_view(["GET", "POST"])
@parser_classes([JSONParser])
def homestay_list_create(request):
    """
    GET  /api/homestays/          → list with filters
    POST /api/homestays/          → create listing (host)
    """
    if request.method == "GET":
        qs = Homestay.objects.filter(is_active=True)

        region = request.query_params.get("region")
        min_price = request.query_params.get("min_price")
        max_price = request.query_params.get("max_price")
        guests = request.query_params.get("guests")
        search = request.query_params.get("search")

        if region:
            qs = qs.filter(region=region)
        if min_price:
            qs = qs.filter(price_per_night__gte=min_price)
        if max_price:
            qs = qs.filter(price_per_night__lte=max_price)
        if guests:
            qs = qs.filter(max_guests__gte=guests)
        if search:
            qs = qs.filter(title__icontains=search) | qs.filter(description__icontains=search)

        try:
            limit = min(int(request.query_params.get("limit", 50)), 200)
        except ValueError:
            limit = 50

        qs = qs[:limit]
        return Response({
            "count": len(qs),
            "results": HomestayListSerializer(qs, many=True).data,
        })

    # POST — create a new listing
    serializer = HomestayCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    homestay = serializer.save()
    return Response(
        HomestayDetailSerializer(homestay).data,
        status=status.HTTP_201_CREATED,
    )


@api_view(["GET"])
def homestay_detail(request, slug):
    """GET /api/homestays/<slug>/"""
    hs = get_object_or_404(Homestay, slug=slug, is_active=True)
    return Response(HomestayDetailSerializer(hs).data)


# ---------- Bookings ----------

@api_view(["GET", "POST"])
@parser_classes([JSONParser])
def homestay_bookings(request, slug):
    """
    GET  /api/homestays/<slug>/bookings/    → host sees inquiries
    POST /api/homestays/<slug>/bookings/    → tourist sends inquiry
    """
    hs = get_object_or_404(Homestay, slug=slug)

    if request.method == "GET":
        qs = hs.bookings.all()
        return Response({
            "count": qs.count(),
            "results": BookingSerializer(qs, many=True).data,
        })

    serializer = BookingSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    booking = serializer.save(homestay=hs)
    return Response(
        BookingSerializer(booking).data,
        status=status.HTTP_201_CREATED,
    )


# ---------- Reviews ----------

@api_view(["GET", "POST"])
@parser_classes([JSONParser])
def homestay_reviews(request, slug):
    """
    GET  /api/homestays/<slug>/reviews/     → list reviews
    POST /api/homestays/<slug>/reviews/     → leave a review
    """
    hs = get_object_or_404(Homestay, slug=slug)

    if request.method == "GET":
        qs = hs.reviews.all()
        return Response({
            "count": qs.count(),
            "results": ReviewSerializer(qs, many=True).data,
        })

    serializer = ReviewSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    review = serializer.save(homestay=hs)

    # Recompute denormalized rating on the homestay
    reviews = hs.reviews.all()
    hs.rating_count = reviews.count()
    hs.rating = round(sum(r.rating for r in reviews) / hs.rating_count, 2) if hs.rating_count else 0.0
    hs.save(update_fields=["rating", "rating_count"])

    return Response(
        ReviewSerializer(review).data,
        status=status.HTTP_201_CREATED,
    )