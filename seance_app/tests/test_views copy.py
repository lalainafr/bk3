from pathlib import Path

from django.conf import settings
from django.test import Client, SimpleTestCase, TestCase
from django.urls import reverse, resolve
from seance_app import views
from seance_app.models import Seance, Salle, Cinema, Film, Evenement
from datetime import date


class TestSeanceCrud(TestCase):
    
   def setUp(self):
    self.cinema = Cinema.objects.create(
        name="Cinema existant"
    )

    
# C I N E M A

    # CREATE

    def test_create_cinema_post_valid(self):
        url = reverse("create_cinema")

        data = {
            "name": "My cinema",
        }

        response = self.client.post(url, data)

        # Vérifie la redirection
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse("list_cinema")
        )

        # Vérifie que le cinéma a été créé
        self.assertTrue(
            Cinema.objects.filter(
                name="My cinema"
            ).exists()
        )

        # Vérifie le message
        messages = list(response.wsgi_request._messages)

        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            "Le cinema a été créé"
        )

    def test_create_cinema_post_invalid(self):
        url = reverse("create_cinema")

        data = {
            # données invalides
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("list_cinema"))

    

    # READ
    
    
    # UPDATE

    def test_update_cinema_get(self):
        url = reverse(
            "update_cinema",
            kwargs={"pk": self.cinema.pk}
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "seance/cinema/update.html"
        )

        self.assertIn("form", response.context)

    def test_update_cinema_post_valid(self):
        url = reverse(
            "update_cinema",
            kwargs={"pk": self.cinema.pk}
        )

        data = {
            "name": "My cinema",
        }

        response = self.client.post(url, data)

        # Vérifie la redirection
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse("list_cinema")
        )

        # Vérifie que le cinéma a été modifié
        self.cinema.refresh_from_db()

        self.assertEqual(
            self.cinema.name,
            "My cinema"
        )

        # Vérifie le message
        messages = list(response.wsgi_request._messages)

        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            "Le cinema a été modifiée"
        )

    def test_update_cinema_post_invalid(self):
        url = reverse(
            "update_cinema",
            kwargs={"pk": self.cinema.pk}
        )

        data = {
            "name": "",
        }

        response = self.client.post(url, data)

        # Vérifie la redirection
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse("list_cinema")
        )

        # Vérifie que le cinéma n'a pas été modifié
        self.cinema.refresh_from_db()

        self.assertEqual(
            self.cinema.name,
            "Cinema existant"
        )

    
    # DELETE
    
    


class TestSeancePage(TestCase, SimpleTestCase):
    
    def setUp(self):
        self.client = Client()

        self.cinema = Cinema.objects.create()
        self.salle = Salle.objects.create(
            cinema=self.cinema,
            numero=1,
            capacite=100,
            )
        self.film = Film.objects.create(
            titre='titre',
            duree=100,
            genre='genre',
            date_sortie = '2026-01-01',
            realisateur = 'realisateur',
            description = 'description',
            affiche = "films/1.jpg"
            )
        self.evenement = Evenement.objects.create(
            titre='titre',
            description = 'description',
            genre='genre',
            affiche = "films/1.jpg"
            )
        
        self.seance = Seance.objects.create(
            film = self.film,
            evenement=self.evenement,
            programme = "programme",
            place_dispo = 1,
            salle = self.salle,
            date_created ='2026-01-01',
            date = '2026-01-01',
            horaire = '10h',
            )
    
# CINEMA

    def test_cinema_create_uses_correct_template(self):
        response = self.client.get(reverse("create_cinema"))
        self.assertTemplateUsed(response,  "seance/cinema/create.html")
        
    def test_cinema_update_uses_correct_template(self):
        response = self.client.get(reverse("update_cinema", args=[self.cinema.pk])
)
        self.assertTemplateUsed(response,  "seance/cinema/update.html")
        
    def test_cinema_list_uses_correct_template(self):
        response = self.client.get(reverse("list_cinema"))
        self.assertTemplateUsed(response,  "seance/cinema/list.html")
    
    def test_cinema_create_url(self):
        url = reverse("create_cinema")
        self.assertEqual(url, "/dashboard/seance/create-cinema/")
        self.assertEqual(resolve(url).func, views.create_cinema)
        
    def test_cinema_list_url(self):
        url = reverse("list_cinema")
        self.assertEqual(url, "/dashboard/seance/list-cinema/")
        self.assertEqual(resolve(url).func, views.list_cinema)
        
    def test_cinema_update_url(self):
        url = reverse("update_cinema", args=[self.cinema.pk])
        self.assertEqual(url, f"/dashboard/seance/update-cinema/{self.cinema.pk}")
        self.assertEqual(resolve(url).func, views.update_cinema)
        
    def test_cinema_delete_url(self):
        url = reverse("delete_cinema", args=[self.cinema.pk])
        self.assertEqual(url, f"/dashboard/seance/delete-cinema/{self.cinema.pk}")
        self.assertEqual(resolve(url).func, views.delete_cinema)

    def test_cinema_create_contains_welcome_message_and_have_correct_status_code(self):
        response = self.client.get(reverse("create_cinema"))
        self.assertContains(
            response,
            "Créer cinéma",
            status_code=200,
        )
  
    def test_cinema_list_contains_welcome_message_and_have_correct_status_code(self):
        response = self.client.get(reverse("list_cinema"))
        self.assertContains(
            response,
            "Liste des Cinemas",
            status_code=200,
        )
  
    def test_cinema_update_contains_welcome_message_and_have_correct_status_code(self):
        response = self.client.get( reverse("update_cinema", args=[self.cinema.pk]))
        self.assertContains(
            response,
            "Modifier cinéma",
            status_code=200,
        )


# SALLE

    def test_salle_create_uses_correct_template(self):
        response = self.client.get(reverse("create_salle"))
        self.assertTemplateUsed(response,  "seance/salle/create.html")
        
    def test_salle_update_uses_correct_template(self):
            response = self.client.get(reverse("update_salle", args=[self.salle.pk])
    )
            self.assertTemplateUsed(response,  "seance/salle/update.html")
        
    def test_salle_list_uses_correct_template(self):
        response = self.client.get(reverse("list_salle"))
        self.assertTemplateUsed(response,  "seance/salle/list.html")
        
    def test_salle_create_url(self):
        url = reverse("create_salle")
        self.assertEqual(url, "/dashboard/seance/create-salle/")
        self.assertEqual(resolve(url).func, views.create_salle)
        
    def test_salle_list_url(self):
        url = reverse("list_salle")
        self.assertEqual(url, "/dashboard/seance/list-salle/")
        self.assertEqual(resolve(url).func, views.list_salle)
        
    def test_salle_update_url(self):
        url = reverse("update_salle", args=[self.salle.pk])
        self.assertEqual(url, f"/dashboard/seance/update-salle/{self.salle.pk}")
        self.assertEqual(resolve(url).func, views.update_salle)
        
    def test_salle_delete_url(self):
        url = reverse("delete_salle", args=[self.salle.pk])
        self.assertEqual(url, f"/dashboard/seance/delete-salle/{self.salle.pk}")
        self.assertEqual(resolve(url).func, views.delete_salle)

    def test_salle_create_contains_welcome_message_and_have_correct_status_code(self):
        response = self.client.get(reverse("create_salle"))
        self.assertContains(
            response,
            "Créer salle",
            status_code=200,
        )
  
    def test_salle_list_contains_welcome_message_and_have_correct_status_code(self):
        response = self.client.get(reverse("list_salle"))
        self.assertContains(
            response,
            "Liste des salles",
            status_code=200,
        )
  
    def test_salle_update_contains_welcome_message_and_have_correct_status_code(self):
            response = self.client.get( reverse("update_salle", args=[self.salle.pk]))
            self.assertContains(
                response,
                "Modifier salle",
                status_code=200,
            )


# FILM

    def test_film_create_uses_correct_template(self):
        response = self.client.get(reverse("create_film"))
        self.assertTemplateUsed(response,  "seance/film/create.html")
        
    def test_film_update_uses_correct_template(self):
        response = self.client.get(reverse("update_film", args=[self.film.pk])
        )
        self.assertTemplateUsed(response,  "seance/film/update.html")
        
    def test_film_list_uses_correct_template(self):
        response = self.client.get(reverse("list_film"))
        self.assertTemplateUsed(response,  "seance/film/list.html")
        
    def test_film_create_url(self):
        url = reverse("create_film")
        self.assertEqual(url, "/dashboard/seance/create-film/")
        self.assertEqual(resolve(url).func, views.create_film)
        
    def test_film_list_url(self):
        url = reverse("list_film")
        self.assertEqual(url, "/dashboard/seance/list-film/")
        self.assertEqual(resolve(url).func, views.list_film)
        
    def test_film_update_url(self):
        url = reverse("update_film", args=[self.film.pk])
        self.assertEqual(url, f"/dashboard/seance/update-film/{self.film.pk}")
        self.assertEqual(resolve(url).func, views.update_film)
        
    def test_film_delete_url(self):
        url = reverse("delete_film", args=[self.film.pk])
        self.assertEqual(url, f"/dashboard/seance/delete-film/{self.film.pk}")
        self.assertEqual(resolve(url).func, views.delete_film)

    def test_film_create_contains_welcome_message_and_have_correct_status_code(self):
        response = self.client.get(reverse("create_film"))
        self.assertContains(
            response,
            "Créer film",
            status_code=200,
        )
  
    def test_film_list_contains_welcome_message_and_have_correct_status_code(self):
        response = self.client.get(reverse("list_film"))
        self.assertContains(
            response,
            "Liste des films",
            status_code=200,
        )
  
    def test_film_update_contains_welcome_message_and_have_correct_status_code(self):
        response = self.client.get( reverse("update_film", args=[self.film.pk]))
        self.assertContains(
            response,
            "Modifier film",
            status_code=200,
        )
    


# EVENEMENT

    def test_evenement_create_uses_correct_template(self):
        response = self.client.get(reverse("create_evenement"))
        self.assertTemplateUsed(response,  "seance/evenement/create.html")
        
    def test_evenement_update_uses_correct_template(self):
        response = self.client.get(reverse("update_evenement", args=[self.evenement.pk]))
        self.assertTemplateUsed(response,  "seance/evenement/update.html")
        
    def test_evenement_list_uses_correct_template(self):
        response = self.client.get(reverse("list_evenement"))
        self.assertTemplateUsed(response,  "seance/evenement/list.html")
    
    def test_evenement_create_url(self):
        url = reverse("create_evenement")
        self.assertEqual(url, "/dashboard/seance/create-evenement/")
        self.assertEqual(resolve(url).func, views.create_evenement)
        
    def test_evenement_list_url(self):
        url = reverse("list_evenement")
        self.assertEqual(url, "/dashboard/seance/list-evenement/")
        self.assertEqual(resolve(url).func, views.list_evenement)
        
    def test_evenement_update_url(self):
        url = reverse("update_evenement", args=[self.evenement.pk])
        self.assertEqual(url, f"/dashboard/seance/update-evenement/{self.evenement.pk}")
        self.assertEqual(resolve(url).func, views.update_evenement)
            
    def test_evenement_delete_url(self):
        url = reverse("delete_evenement", args=[self.evenement.pk])
        self.assertEqual(url, f"/dashboard/seance/delete-evenement/{self.evenement.pk}")
        self.assertEqual(resolve(url).func, views.delete_evenement)

    def test_evenement_create_contains_welcome_message_and_have_correct_status_code(self):
        response = self.client.get(reverse("create_evenement"))
        self.assertContains(
            response,
            "Créer evenement",
            status_code=200,
        )
  
    def test_evenement_list_contains_welcome_message_and_have_correct_status_code(self):
        response = self.client.get(reverse("list_evenement"))
        self.assertContains(
            response,
            "Liste des evenements",
            status_code=200,
        )
  
    def test_evenement_update_contains_welcome_message_and_have_correct_status_code(self):
            response = self.client.get( reverse("update_evenement", args=[self.evenement.pk]))
            self.assertContains(
                response,
                "Modifier evenement",
                status_code=200,
            )


# SEANCE

    def test_seance_create_uses_correct_template(self):
        response = self.client.get(reverse("create_seance"))
        self.assertTemplateUsed(response,  "seance/seance/create.html")
        
    def test_seance_update_uses_correct_template(self):
        response = self.client.get(reverse("update_seance", args=[self.seance.pk]))
        self.assertTemplateUsed(response,  "seance/seance/update.html")
        
    def test_seance_list_uses_correct_template(self):
        response = self.client.get(reverse("list_seance"))
        self.assertTemplateUsed(response,  "seance/seance/list.html")
        
    def test_seance_create_url(self):
        url = reverse("create_seance")
        self.assertEqual(url, "/dashboard/seance/create/")
        self.assertEqual(resolve(url).func, views.create_seance)
        
    def test_seance_list_url(self):
        url = reverse("list_seance")
        self.assertEqual(url, "/dashboard/seance/list/")
        self.assertEqual(resolve(url).func, views.list_seance)
        
    def test_seance_delete_url(self):
           url = reverse("delete_seance", args=[self.seance.pk])
           self.assertEqual(url, f"/dashboard/seance/delete/{self.seance.pk}")
           self.assertEqual(resolve(url).func, views.delete_seance)

    def test_seance_update_url(self):
            url = reverse("update_seance", args=[self.seance.pk])
            self.assertEqual(url, f"/dashboard/seance/update/{self.seance.pk}")
            self.assertEqual(resolve(url).func, views.update_seance)
            
   
    def test_seance_create_contains_welcome_message_and_have_correct_status_code(self):
        response = self.client.get(reverse("create_seance"))
        self.assertContains(
            response,
            "Créer seance",
            status_code=200,
        )

    def test_seance_create_contains_welcome_message_and_have_correct_status_code(self):
        response = self.client.get(reverse("create_seance"))
        self.assertContains(
            response,
            " Programmer une séance",
            status_code=200,
        )
  
    def test_seance_list_contains_welcome_message_and_have_correct_status_code(self):
        response = self.client.get(reverse("list_seance"))
        self.assertContains(
            response,
            "Liste des seances",
            status_code=200,
        )
  
    def test_seance_update_contains_welcome_message_and_have_correct_status_code(self):
        response = self.client.get( reverse("update_seance", args=[self.seance.pk]))
        self.assertContains(
            response,
            "Modifier une séance",
            status_code=200,
        )

