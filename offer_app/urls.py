from django.urls import path
from . import views

urlpatterns = [
    # Offer
    path("", views.list_offer, name="list_offer"),
    # path("detail_dispo/", views.detail_dispo, name="detail_dispo"),
    
]
