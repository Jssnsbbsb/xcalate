from django.urls import path
from . import views

urlpatterns = [
    path("", views.homestay_list_create, name="homestay-list-create"),
    path("<slug:slug>/", views.homestay_detail, name="homestay-detail"),
    path("<slug:slug>/bookings/", views.homestay_bookings, name="homestay-bookings"),
    path("<slug:slug>/reviews/", views.homestay_reviews, name="homestay-reviews"),
]