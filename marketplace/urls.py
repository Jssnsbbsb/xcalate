from django.urls import path

from . import views


urlpatterns = [
    path("listings/", views.listing_list_create, name="listing-list-create"),
    path(
        "listings/<slug:slug>/contact/",
        views.contact_seller,
        name="contact-seller",
    ),
    path("listings/<slug:slug>/", views.listing_detail, name="listing-detail"),
    path("my-listings/", views.my_listings, name="my-listings"),
    path("my-contacts/", views.my_contacts, name="my-contacts"),
    path("categories/", views.listing_categories, name="listing-categories"),
]
