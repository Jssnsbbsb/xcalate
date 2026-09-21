"""
URL configuration for xcalate project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.http import JsonResponse
from django.urls import path, include


def root(request):
    return JsonResponse({
        "name": "xcalate API",
        "endpoints": {
            "directory": [
                {"method": "GET", "path": "/"},
            ],
            "admin": [
                {"method": "GET", "path": "/admin/"},
            ],
            "authentication": [
                {"method": "POST", "path": "/api/auth/register/"},
                {"method": "POST", "path": "/api/auth/login/"},
                {"method": "POST", "path": "/api/auth/refresh/"},
                {"method": "GET", "path": "/api/auth/me/"},
                {"method": "PATCH", "path": "/api/auth/me/"},
            ],
            "marketplace": [
                {"method": "GET", "path": "/api/marketplace/listings/"},
                {"method": "POST", "path": "/api/marketplace/listings/"},
                {"method": "GET", "path": "/api/marketplace/listings/<slug>/"},
                {"method": "POST", "path": "/api/marketplace/listings/<slug>/contact/"},
                {"method": "GET", "path": "/api/marketplace/my-listings/"},
                {"method": "GET", "path": "/api/marketplace/my-contacts/"},
                {"method": "GET", "path": "/api/marketplace/categories/"},
            ],
            "places": [
                {"method": "GET", "path": "/api/places/"},
                {"method": "GET", "path": "/api/places/categories/"},
                {"method": "GET", "path": "/api/places/<slug>/"},
            ],
            "regions": [
                {"method": "GET", "path": "/api/regions/"},
                {"method": "GET", "path": "/api/regions/<slug>/"},
                {"method": "GET", "path": "/api/regions/<slug>/download/"},
            ],
            "homestays": [
                {"method": "GET", "path": "/api/homestays/"},
                {"method": "POST", "path": "/api/homestays/"},
                {"method": "GET", "path": "/api/homestays/<slug>/"},
                {"method": "GET", "path": "/api/homestays/<slug>/bookings/"},
                {"method": "POST", "path": "/api/homestays/<slug>/bookings/"},
                {"method": "GET", "path": "/api/homestays/<slug>/reviews/"},
                {"method": "POST", "path": "/api/homestays/<slug>/reviews/"},
            ],
            "companion": [
                {"method": "POST", "path": "/api/companion/ask/"},
            ],
            "api": [
                {"method": "GET", "path": "/api/health/"},
                {"method": "GET", "path": "/api/languages/"},
                {"method": "GET", "path": "/api/voices/"},
                {"method": "POST", "path": "/api/voice/translate/"},
                {"method": "POST", "path": "/api/text/translate/"},
                {"method": "POST", "path": "/api/text/tts/"},
            ],
        },
    })


urlpatterns = [
    path("", root, name="api-root"),
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),
    path("api/auth/", include("users.urls")),
    path("api/places/", include("places.urls")),
    path("api/regions/", include("regions.urls")),
    path("api/homestays/", include("homestays.urls")),
    path("api/companion/", include("companion.urls")),   # 👈 NEW
    path("api/marketplace/", include("marketplace.urls")),





]
