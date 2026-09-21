from rest_framework import serializers

from .models import ContactRequest, Listing
from users.models import User


class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "phone", "business_name", "region"]
        read_only_fields = fields


class ListingListSerializer(serializers.ModelSerializer):
    seller_username = serializers.CharField(
        source="user.username",
        read_only=True,
    )

    class Meta:
        model = Listing
        fields = [
            "id",
            "title",
            "slug",
            "type",
            "short_description",
            "price",
            "price_unit",
            "images",
            "region",
            "category",
            "is_featured",
            "seller_username",
        ]
        read_only_fields = fields


class ListingDetailSerializer(serializers.ModelSerializer):
    seller = SellerSerializer(source="user", read_only=True)

    class Meta:
        model = Listing
        fields = [
            "id",
            "user",
            "seller",
            "type",
            "title",
            "slug",
            "description",
            "short_description",
            "price",
            "price_unit",
            "images",
            "region",
            "category",
            "contact_phone",
            "contact_email",
            "whatsapp",
            "is_active",
            "is_featured",
            "view_count",
            "created_at",
            "updated_at",
        ]
        read_only_fields = fields


class ListingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = [
            "type",
            "title",
            "description",
            "short_description",
            "price",
            "price_unit",
            "images",
            "region",
            "category",
            "contact_phone",
            "contact_email",
            "whatsapp",
            "is_active",
            "is_featured",
        ]
        extra_kwargs = {
            "images": {"required": False},
            "contact_email": {"required": False, "allow_blank": True},
            "whatsapp": {"required": False, "allow_blank": True},
            "is_active": {"required": False},
            "is_featured": {"required": False},
        }

    def validate_type(self, value):
        if value not in {"product", "service"}:
            raise serializers.ValidationError(
                "Type must be either 'product' or 'service'."
            )
        return value

    def validate_images(self, value):
        if not isinstance(value, list):
            raise serializers.ValidationError("Images must be a list of URLs.")
        if len(value) > 10:
            raise serializers.ValidationError(
                "A listing can have at most 10 images."
            )
        return value

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than 0.")
        return value

    def create(self, validated_data):
        request = self.context["request"]
        return Listing.objects.create(user=request.user, **validated_data)


class ContactRequestSerializer(serializers.ModelSerializer):
    listing_title = serializers.CharField(
        source="listing.title",
        read_only=True,
    )

    class Meta:
        model = ContactRequest
        fields = [
            "id",
            "listing",
            "listing_title",
            "name",
            "phone",
            "email",
            "message",
            "created_at",
        ]
        read_only_fields = ["id", "listing", "listing_title", "created_at"]
        extra_kwargs = {
            "email": {"required": False, "allow_blank": True},
        }
