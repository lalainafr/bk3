from django.urls import path

from . import views

urlpatterns = [
    path("", views.main_dashboard, name="main_dashboard"),
    path(
        "remplissage-seance/",
        views.dashboard_remplissage_seance,
        name="dashboard_remplissage_seance",
    ),
    path(
        "remplissage-salle/",
        views.dashboard_remplissage_salle,
        name="dashboard_remplissage_salle",
    ),
    path(
        "remplissage-creneau/",
        views.dashboard_remplissage_creneau,
        name="dashboard_remplissage_creneau",
    ),
    path("all-ticket-list/", views.all_ticket_list, name="all_ticket_list"),
]
