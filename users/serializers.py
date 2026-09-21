from rest_framework import serializers

from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=(User.Role.TOURIST, User.Role.LOCAL))
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password",
            "role",
            "phone",
            "region",
        )
        extra_kwargs = {
            "email": {"required": False, "allow_blank": True},
            "region": {"required": False, "allow_blank": True},
        }

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "role",
            "phone",
            "region",
            "bio",
            "avatar_url",
            "business_name",
        )
        read_only_fields = fields


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "email",
            "phone",
            "region",
            "bio",
            "avatar_url",
            "business_name",
        )
        extra_kwargs = {
            "email": {"required": False, "allow_blank": True},
            "phone": {"required": False},
            "region": {"required": False, "allow_blank": True},
            "bio": {"required": False, "allow_blank": True},
            "avatar_url": {"required": False, "allow_blank": True},
            "business_name": {"required": False, "allow_blank": True},
        }
