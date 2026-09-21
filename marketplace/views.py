from decimal import Decimal, InvalidOperation

from django.db.models import F, Q
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.permissions import IsLocal

from .models import ContactRequest, Listing
from .serializers import (
	ListingCreateSerializer,
	ListingDetailSerializer,
	ListingListSerializer,
)


def _require_permission(request, permission_class, message=None):
	permission = permission_class()
	if not permission.has_permission(request, None):
		raise PermissionDenied(message or permission.message)


def _parse_decimal(value, parameter_name):
	try:
		return Decimal(value)
	except (InvalidOperation, TypeError):
		raise ValidationError(f"{parameter_name} must be a valid number.")


@api_view(["GET", "POST"])
def listing_list_create(request):
	if request.method == "GET":
		queryset = Listing.objects.filter(is_active=True).select_related("user")

		listing_type = request.query_params.get("type")
		region = request.query_params.get("region")
		category = request.query_params.get("category")
		search = request.query_params.get("search")
		min_price = request.query_params.get("min_price")
		max_price = request.query_params.get("max_price")
		featured = request.query_params.get("featured")

		if listing_type:
			queryset = queryset.filter(type=listing_type)
		if region:
			queryset = queryset.filter(region=region)
		if category:
			queryset = queryset.filter(category=category)
		if search:
			queryset = queryset.filter(
				Q(title__icontains=search)
				| Q(description__icontains=search)
				| Q(short_description__icontains=search)
			)
		if min_price:
			queryset = queryset.filter(
				price__gte=_parse_decimal(min_price, "min_price")
			)
		if max_price:
			queryset = queryset.filter(
				price__lte=_parse_decimal(max_price, "max_price")
			)
		if featured:
			featured_value = featured.lower()
			if featured_value in {"true", "1", "yes"}:
				queryset = queryset.filter(is_featured=True)
			elif featured_value in {"false", "0", "no"}:
				queryset = queryset.filter(is_featured=False)

		try:
			limit = min(max(int(request.query_params.get("limit", 50)), 1), 200)
		except (TypeError, ValueError):
			limit = 50

		queryset = queryset[:limit]
		return Response({
			"count": len(queryset),
			"results": ListingListSerializer(queryset, many=True).data,
		})

	_require_permission(request, IsLocal)
	serializer = ListingCreateSerializer(
		data=request.data,
		context={"request": request},
	)
	serializer.is_valid(raise_exception=True)
	listing = serializer.save()
	return Response(
		ListingDetailSerializer(listing).data,
		status=status.HTTP_201_CREATED,
	)


@api_view(["GET"])
def listing_detail(request, slug):
	listing = get_object_or_404(
		Listing.objects.select_related("user"),
		slug=slug,
		is_active=True,
	)

	Listing.objects.filter(pk=listing.pk).update(view_count=F("view_count") + 1)
	listing.refresh_from_db(fields=["view_count"])

	return Response(ListingDetailSerializer(listing).data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_listings(request):
	queryset = Listing.objects.filter(user=request.user).select_related("user")
	return Response(ListingDetailSerializer(queryset, many=True).data)


@api_view(["GET"])
def listing_categories(request):
	return Response({
		"products": [
			value for value, label in Listing.PRODUCT_CATEGORY_CHOICES
		],
		"services": [
			value for value, label in Listing.SERVICE_CATEGORY_CHOICES
		],
	})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def contact_seller(request, slug):
	listing = get_object_or_404(
		Listing,
		slug=slug,
		is_active=True,
	)
	serializer = ContactRequestSerializer(data=request.data)
	serializer.is_valid(raise_exception=True)
	contact_request = serializer.save(
		listing=listing,
		user=request.user,
	)

	return Response(
		{
			"id": contact_request.id,
			"created_at": contact_request.created_at,
			"message": "Seller will contact you",
		},
		status=status.HTTP_201_CREATED,
	)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_contacts(request):
	queryset = ContactRequest.objects.filter(
		listing__user=request.user,
	).select_related("listing", "user")
	return Response(ContactRequestSerializer(queryset, many=True).data)
