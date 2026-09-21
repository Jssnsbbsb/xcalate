from rest_framework.permissions import BasePermission
from rest_framework.permissions import SAFE_METHODS


class IsTourist(BasePermission):
    message = "Tourist access is required."

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role == "tourist"
        )


class IsLocal(BasePermission):
    message = "Local user access is required."

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role == "local"
        )


class IsAdmin(BasePermission):
    message = "Administrator access is required."

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role == "admin"
        )


class IsLocalOrReadOnly(BasePermission):
    message = "Only local users can modify this resource."

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role == "local"
        )


class IsOwnerOrReadOnly(BasePermission):
    message = "Only the owner can modify this resource."

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        if not request.user or not request.user.is_authenticated:
            return False

        owner = getattr(obj, "user", None)
        if owner is None:
            owner = getattr(obj, "owner", None)

        return owner == request.user
