from django.urls import path
from . import views

urlpatterns = [
    path("", views.region_list, name="region-list"),
    path("<slug:slug>/", views.region_detail, name="region-detail"),
    path("<slug:slug>/download/", views.region_download, name="region-download"),
]