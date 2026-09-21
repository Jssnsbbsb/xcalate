from django.urls import path
from . import views

urlpatterns = [
    path("", views.place_list, name="place-list"),
    path("categories/", views.place_categories, name="place-categories"),
    path("<slug:slug>/", views.place_detail, name="place-detail"),
]