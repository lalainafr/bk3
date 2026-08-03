from django.urls import path
from . import views

urlpatterns = [
    # Offer
    path("film/", views.list_offer_film, name="list_offer_film"),
    path("evenement/", views.list_offer_evenement, name="list_offer_evenement"),
    # path("detail/<str:pk>/", views.detail_offer, name="detail_offer"),
    # path("detail_dispo/", views.detail_dispo, name="detail_dispo"),
    
]
