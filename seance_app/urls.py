from django.urls import path
from . import views

urlpatterns = [
    # seance
    path("create/", views.create_seance, name="create_seance"),
    path("update/<str:pk>", views.update_seance, name="update_seance"),
    path("list/", views.list_seance, name="list_seance"),
    path("delete/<str:pk>", views.delete_seance, name="delete_seance"),
    # cinema
    path("create-cinema/", views.create_cinema, name="create_cinema"),
    path("update-cinema/<str:pk>", views.update_cinema, name="update_cinema"),
    path("list-cinema/", views.list_cinema, name="list_cinema"),
    path("delete-cinema/<str:pk>", views.delete_cinema, name="delete_cinema"),
    # salle
    path("create-salle/", views.create_salle, name="create_salle"),
    path("update-salle/<str:pk>", views.update_salle, name="update_salle"),
    path("list-salle/", views.list_salle, name="list_salle"),
    path("delete-salle/<str:pk>", views.delete_salle, name="delete_salle"),
    # film
    path("create-film/", views.create_film, name="create_film"),
    path("update-film/<str:pk>", views.update_film, name="update_film"),
    path("detail-film/<str:pk>", views.detail_film, name="detail_film"),
    path("list-film/", views.list_film, name="list_film"),
    path("delete-film/<str:pk>", views.delete_film, name="delete_film"),
    # evenement
    path("create-evenement/", views.create_evenement, name="create_evenement"),
    path("update-evenement/<str:pk>", views.update_evenement, name="update_evenement"),
    path("list-evenement/", views.list_evenement, name="list_evenement"),
    path("delete-evenement/<str:pk>", views.delete_evenement, name="delete_evenement"),
]
