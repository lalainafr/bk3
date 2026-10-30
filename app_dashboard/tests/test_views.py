from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponse
from django.test import RequestFactory, TestCase

from app_dashboard.views import (all_ticket_list,
                                 dashboard_remplissage_creneau,
                                 dashboard_remplissage_salle,
                                 dashboard_remplissage_seance, main_dashboard)


class DashboardTests(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

        # Utilisateur administrateur fictif
        self.admin = SimpleNamespace(is_authenticated=True, is_staff=True)

        # Utilisateur non administrateur
        self.user = SimpleNamespace(is_authenticated=True, is_staff=False)

    # TEST 1 : Affichage du tableau de bord
    @patch("app_dashboard.views.render")
    def test_main_dashboard(self, mock_render):

        request = self.factory.get("/dashboard/")
        request.user = self.admin

        mock_render.return_value = HttpResponse("OK")

        response = main_dashboard(request)

        self.assertEqual(response.status_code, 200)
        mock_render.assert_called_once_with(request, "dashboard/main_dashboard.html")

    # TEST 2 : Calcul du taux de remplissage d'une séance
    @patch("app_dashboard.views.render")
    @patch("app_dashboard.views.Seance.objects.select_related")
    def test_dashboard_remplissage_seance(self, mock_seances, mock_render):

        request = self.factory.get("/dashboard/seances/")
        request.user = self.admin

        salle = SimpleNamespace(capacite=100)
        seance = SimpleNamespace(salle=salle, place_dispo=40, evenement=None)

        mock_seances.return_value = [seance]
        mock_render.return_value = HttpResponse("OK")

        response = dashboard_remplissage_seance(request)

        self.assertEqual(response.status_code, 200)

        resultats = mock_render.call_args[0][2]["resultats"]

        self.assertEqual(len(resultats), 1)
        self.assertEqual(resultats[0]["capacite"], 100)
        self.assertEqual(resultats[0]["disponibles"], 40)
        self.assertEqual(resultats[0]["taux"], 60.0)

    # TEST 3 : Calcul du taux de remplissage des salles
    @patch("app_dashboard.views.render")
    @patch("app_dashboard.views.Seance.objects.select_related")
    def test_dashboard_remplissage_salle(self, mock_seances, mock_render):

        request = self.factory.get("/dashboard/salles/")
        request.user = self.admin

        salle = SimpleNamespace(id=1, capacite=100)

        seance1 = SimpleNamespace(salle=salle, place_dispo=40)

        seance2 = SimpleNamespace(salle=salle, place_dispo=20)

        mock_seances.return_value = [seance1, seance2]
        mock_render.return_value = HttpResponse("OK")

        response = dashboard_remplissage_salle(request)

        self.assertEqual(response.status_code, 200)

        resultats = mock_render.call_args[0][2]["resultats"]

        self.assertEqual(len(resultats), 1)
        self.assertEqual(resultats[0]["capacite"], 200)
        self.assertEqual(resultats[0]["disponibles"], 60)
        self.assertEqual(resultats[0]["nb_seances"], 2)
        self.assertEqual(resultats[0]["taux"], 70.0)

    # TEST 4 : Statistiques de remplissage par créneau
    @patch("app_dashboard.views.render")
    @patch("app_dashboard.views.Seance.objects.filter")
    def test_dashboard_remplissage_creneau(self, mock_filter, mock_render):

        request = self.factory.get("/dashboard/creneaux/")
        request.user = self.admin

        donnees = [
            {"capacite_totale": 100, "places_disponibles": 20},
            {"capacite_totale": 100, "places_disponibles": 40},
            {"capacite_totale": 0, "places_disponibles": 0},
            {"capacite_totale": 80, "places_disponibles": 0},
        ]

        queryset = MagicMock()
        queryset.aggregate.side_effect = donnees
        mock_filter.return_value = queryset

        mock_render.return_value = HttpResponse("OK")

        response = dashboard_remplissage_creneau(request)

        self.assertEqual(response.status_code, 200)

        resultats = mock_render.call_args[0][2]["resultats"]

        self.assertEqual(len(resultats), 4)

        # Premier créneau : 80 % de remplissage
        self.assertEqual(resultats[0]["taux"], 80.0)

        # Deuxième créneau : 60 % de remplissage
        self.assertEqual(resultats[1]["taux"], 60.0)

        # Troisième créneau : aucune capacité
        self.assertEqual(resultats[2]["taux"], 0)

        # Quatrième créneau : 100 % de remplissage
        self.assertEqual(resultats[3]["taux"], 100.0)

    # TEST 5 : Affichage de tous les tickets
    @patch("app_dashboard.views.render")
    @patch("app_dashboard.views.Ticket.objects.all")
    def test_all_ticket_list(self, mock_tickets, mock_render):

        request = self.factory.get("/dashboard/tickets/")
        request.user = self.admin

        ticket = SimpleNamespace(
            payment=SimpleNamespace(orders=["Commande 1", "Commande 2"])
        )

        mock_tickets.return_value = [ticket]
        mock_render.return_value = HttpResponse("OK")

        response = all_ticket_list(request)

        self.assertEqual(response.status_code, 200)

        context = mock_render.call_args[0][2]

        self.assertEqual(len(context["tickets"]), 1)
        self.assertTrue(hasattr(ticket, "orders_formatted"))

    # TEST 6 : Vérifier le refus d'accès à un utilisateur non admin
    def test_access_refused_non_staff(self):

        request = self.factory.get("/dashboard/")
        request.user = self.user

        response = main_dashboard(request)

        self.assertEqual(response.status_code, 302)

    # TEST 7 : Vérifier le refus d'accès à un utilisateur anonyme
    def test_access_refused_anonymous(self):

        request = self.factory.get("/dashboard/")
        request.user = AnonymousUser()

        response = main_dashboard(request)

        self.assertEqual(response.status_code, 302)
