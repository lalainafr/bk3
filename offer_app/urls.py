from django.urls import path

from . import views

urlpatterns = [
    # Offer
    path("film/", views.list_offer_film, name="list_offer_film"),
    path("evenement/", views.list_offer_evenement, name="list_offer_evenement"),
    path("creneau-film/<str:pk>/", views.creneau_film, name="creneau_film"),
    path(
        "creaneu-evenement/<str:pk>/", views.creneau_evenement, name="creneau_evenement"
    ),
    path("creneau-film/<str:pk>/", views.creneau_film, name="creneau_film"),
]
