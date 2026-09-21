from django.urls import path

from .views import login_view, me_view, refresh_view, register_view


urlpatterns = [
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("refresh/", refresh_view, name="refresh"),
    path("me/", me_view, name="me"),
]
