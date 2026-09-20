from django.urls import path
from . import views

urlpatterns = [
    # Offer
    path("film/", views.list_offer_film, name="list_offer_film"),
    path("evenement/", views.list_offer_evenement, name="list_offer_evenement"),
    path("film-list-seance/<str:pk>/",views.film_list_seance, name="film_list_seance"),
    path("evenement-list-seance/<str:pk>/",views.evenement_list_seance, name="evenement_list_seance"),
    
]
