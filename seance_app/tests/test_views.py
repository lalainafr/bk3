from pathlib import Path

from django.conf import settings
from django.test import Client, SimpleTestCase, TestCase
from django.urls import reverse, resolve
from seance_app import views
from seance_app.models import Seance, Salle, Cinema, Film, Evenement
from datetime import date

from io import BytesIO

from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image

class TestSeancePage(TestCase, SimpleTestCase):
    
    def setUp(self):
        self.client = Client()

        self.cinema = Cinema.objects.create(
            nom="My cinema", 
            adresse="Paris", 
            telephone="0123456789",
        )
        self.salle = Salle.objects.create(
           cinema=self.cinema, 
           numero=1, 
           capacite=100,
           disponible=True,
            )
        self.film = Film.objects.create(
            titre='titre',
            duree=4,
            genre='genre',
            date_sortie = '2026-01-02',
            realisateur = 'realisateur',
            description = 'description',
            affiche = "films/2.jpg"
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
            date_created ='2026-01-02',
            date = '2026-01-02',
            horaire = '11h',
            )
    
# ------- CINEMA --------
                    
    ### CREATE
        
    def test_create_cinema_post_valid(self):
        url = reverse("create_cinema")

        data = {
            "nom": "My cinema",
            "adresse": "Paris",
            "telephone": "0123456789",

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
                nom ="My cinema",
                adresse= "Paris",
                telephone ="0123456789",
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

    ### READ

    def test_list_seance(self):
        url = reverse("list_seance")

        response = self.client.get(url)

        # Vérifie que la page fonctionne
        self.assertEqual(response.status_code, 200)

        # Vérifie le template utilisé
        self.assertTemplateUsed(
            response,
            "seance/seance/list.html"
        )

        # Vérifie que les séances sont présentes dans le contexte
        self.assertIn("seances", response.context)

        # Vérifie que la séance créée est dans la liste
        self.assertIn(
            self.seance,
            response.context["seances"]
        )

    
    ### UPDATE

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
           "nom": "My updated cinema", "adresse": "Paris", "telephone": "0123456789",
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
            self.cinema.nom,
            "My updated cinema"
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
            "nom": "", "adresse": "Paris", "telephone": "0123456789",

        }

        response = self.client.post(url, data)

        # Vérifie la redirection
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse("list_cinema")
        )
        
    
    ### DELETE

    def test_delete_cinema(self):
        url = reverse(
            "delete_cinema",
            kwargs={"pk": self.cinema.pk}
        )

        response = self.client.get(url)

        # Vérifie la redirection
        self.assertEqual(response.status_code, 302)

        self.assertRedirects(
            response,
            reverse("list_cinema")
        )

        # Vérifie que le cinéma a été supprimé
        self.assertFalse(
            Cinema.objects.filter(
                pk=self.cinema.pk
            ).exists()
        )

        # Vérifie le message
        messages = list(response.wsgi_request._messages)

        self.assertEqual(len(messages), 1)

        self.assertEqual(
            str(messages[0]),
            "Le cinema a été supprimé"
        )


# ------- SALLE --------
 
   ### CREATE
        
    def test_create_salle_post_valid(self):
        url = reverse("create_salle")

        data = {
            "cinema": self.cinema.pk,
            "numero":2,
            "capacite":120,
        }
        
        response = self.client.post(url, data)

        # Vérifie la redirection
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse("list_salle")
        )

        # Vérifie que le cinéma a été créé
        self.assertTrue(
            Salle.objects.filter(
                cinema= self.cinema,
                numero=2,
                capacite=120,
            ).exists()
        )

        # Vérifie le message
        messages = list(response.wsgi_request._messages)

        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            "La salle a été créée"
        )

    def test_create_salle_post_invalid(self):
        url = reverse("create_salle")

        data = {
            # données invalides
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("list_salle"))

    ### READ

    # def test_list_salle(self):
        url = reverse("list_salle")

        response = self.client.get(url)

        # Vérifie que la page fonctionne
        self.assertEqual(response.status_code, 200)

        # Vérifie le template utilisé
        self.assertTemplateUsed(
            response,
            "seance/salle/list.html"
        )

        # Vérifie que les séances sont présentes dans le contexte
        self.assertIn("salles", response.context)

        # Vérifie que la séance créée est dans la liste
        self.assertIn(
            self.salle,
            response.context["salles"]
        )

    
    ### UPDATE

    def test_update_salle_get(self):
        url = reverse(
            "update_salle",
            kwargs={"pk": self.salle.pk}
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "seance/salle/update.html"
        )

        self.assertIn("form", response.context)

    # def test_update_salle_post_valid(self):
        url = reverse(
            "update_salle",
            kwargs={"pk": self.salle.pk}
        )

        data = {
            "cinema":self.cinema, 
            "numero":1, 
            "capacite":100,        
            "disponible":True,        
            }

        response = self.client.post(url, data)

        # Vérifie la redirection
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse("list_salle")
        )

        # Vérifie que le cinéma a été modifié
        self.salle.refresh_from_db()

        self.assertEqual(
            self.salle.numero,
            1
        )


    def test_update_salle_post_invalid(self):
        url = reverse(
            "update_salle",
            kwargs={"pk": self.salle.pk}
        )

        data = {
            "cinema": "", "numero": "", "capacite": "", "disponibilite": True
        }

        response = self.client.post(url, data)

        # Vérifie la redirection
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse("list_salle")
        )
        
    
    ### DELETE

    def test_delete_salle(self):
        url = reverse(
            "delete_salle",
            kwargs={"pk": self.salle.pk}
        )

        response = self.client.get(url)

        # Vérifie la redirection
        self.assertEqual(response.status_code, 302)

        self.assertRedirects(
            response,
            reverse("list_salle")
        )

        # Vérifie que le cinéma a été supprimé
        self.assertFalse(
            Salle.objects.filter(
                pk=self.salle.pk
            ).exists()
        )

        # Vérifie le message
        messages = list(response.wsgi_request._messages)

        self.assertEqual(len(messages), 1)

        self.assertEqual(
            str(messages[0]),
            "La salle a été supprimée"
        )

# ------- FILM --------
 
   ### CREATE

    def test_create_film_post_valid(self):

        url = reverse("create_film")

        # Création d'une vraie petite image JPEG pour le test
        image = Image.new("RGB", (100, 100))
        image_io = BytesIO()
        image.save(image_io, format="JPEG")

        uploaded_image = SimpleUploadedFile(
            "1.jpg",
            image_io.getvalue(),
            content_type="image/jpeg",
        )

        data = {
            "titre": "My titre",
            "duree": 2,
            "genre": "My genre",
            "date_sortie": "2026-01-01",
            "realisateur": "My realisateur",
            "description": "My description",
            "affiche": uploaded_image,
        }

        response = self.client.post(url, data)

        # Vérifie la redirection
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse("list_film")
        )

        # Vérifie que le film a été créé
        film = Film.objects.filter(titre="My titre").first()

        self.assertIsNotNone(film)
        self.assertEqual(film.duree, 2)
        self.assertEqual(film.genre, "My genre")
        self.assertEqual(str(film.date_sortie), "2026-01-01")
        self.assertEqual(film.realisateur, "My realisateur")
        self.assertEqual(film.description, "My description")

        # Vérifie que l'affiche a bien été enregistrée
        self.assertTrue(film.affiche)
        self.assertTrue(film.affiche.name.startswith("films/"))
        # Vérifie le message
        messages = list(response.wsgi_request._messages)

        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            "Le film a été créé"
        )

    

    def test_create_film_post_invalid(self):
        url = reverse("create_film")

        data = {
            # données invalides
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("list_film"))

    ### READ

    def test_list_film(self):
        url = reverse("list_film")

        response = self.client.get(url)

        # Vérifie que la page fonctionne
        self.assertEqual(response.status_code, 200)

        # Vérifie le template utilisé
        self.assertTemplateUsed(
            response,
            "seance/film/list.html"
        )

        # Vérifie que les films sont présentes dans le contexte
        self.assertIn("films", response.context)

        # Vérifie que le film créé est dans la liste
        self.assertIn(
            self.film,
            response.context["films"]
        )

    
    # ### UPDATE

    def test_update_film_get(self):
        url = reverse(
            "update_film",
            kwargs={"pk": self.film.pk}
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "seance/film/update.html"
        )

        self.assertIn("form", response.context)

    # def test_update_film_post_valid(self):
        url = reverse(
            "update_film",
            kwargs={"pk": self.film.pk}
        )
        
        # Création d'une vraie image JPEG  
        image = Image.new("RGB", (100, 100))
        
        image_io = BytesIO() 
        image.save(image_io, format="JPEG") 
        uploaded_image = SimpleUploadedFile( "1.jpg", 
        image_io.getvalue(), content_type="image/jpeg", )

        data = {
            "titre": "titre",
            "duree": 2,
            "genre": "My genre",
            "date_sortie": "2026-01-01",
            "realisateur": "My realisateur",
            "description": "My description",
            "affiche": uploaded_image,       
            }

        response = self.client.post(url, data)

        # Vérifie la redirection
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse("list_film")
        )

        # Vérifie que le film a été modifié
        self.film.refresh_from_db()

        self.assertEqual(
            self.film.titre,
            "titre"
        )


    def test_update_salle_post_invalid(self):
        url = reverse(
            "update_film",
            kwargs={"pk": self.film.pk}
        )

        # Création d'une vraie image JPEG      
        image = Image.new("RGB", (100, 100))
        
        image_io = BytesIO() 
        image.save(image_io, format="JPEG") 
        uploaded_image = SimpleUploadedFile( "1.jpg", 
        image_io.getvalue(), content_type="image/jpeg", )


        data = {
            "titre": "titre",
            "duree": 2,
            "genre": "My genre",
            "date_sortie": "2026-01-01",
            "realisateur": "My realisateur",
            "description": "My description",
            "affiche": uploaded_image,       
            }

        response = self.client.post(url, data)

        # Vérifie la redirection
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse("list_film")
        )
        
    
    ### DELETE

    def test_delete_film(self):
        url = reverse(
            "delete_film",
            kwargs={"pk": self.film.pk}
        )

        response = self.client.get(url)

        # Vérifie la redirection
        self.assertEqual(response.status_code, 302)

        self.assertRedirects(
            response,
            reverse("list_film")
        )

        # Vérifie le message
        messages = list(response.wsgi_request._messages)

        self.assertEqual(len(messages), 1)

        self.assertEqual(
            str(messages[0]),
            "Le film a été supprimé"
        )

# ------- EVENEMENT --------


   ### CREATE

    def test_create_evenement_post_valid(self):

        url = reverse("create_evenement")

        # Création d'une vraie petite image JPEG pour le test
        image = Image.new("RGB", (100, 100))
        image_io = BytesIO()
        image.save(image_io, format="JPEG")

        uploaded_image = SimpleUploadedFile(
            "1.jpg",
            image_io.getvalue(),
            content_type="image/jpeg",
        )

        data = {
            "titre": "My titre",

            "genre": "My genre",
            "date_sortie": "2026-01-01",
            "description": "My description",
            "affiche": uploaded_image,
        }

        response = self.client.post(url, data)

        # Vérifie la redirection
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse("list_evenement")
        )

        # Vérifie que le evenement a été créé
        evenement = Evenement.objects.filter(titre="My titre").first()

        self.assertIsNotNone(evenement)
        self.assertEqual(evenement.genre, "My genre")
        self.assertEqual(evenement.description, "My description")

        # Vérifie que l'affiche a bien été enregistrée
        self.assertTrue(evenement.affiche)
        self.assertTrue(evenement.affiche.name.startswith("evenements/"))
        # Vérifie le message
        messages = list(response.wsgi_request._messages)

        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            "L'evenement a été créé"
        )


    def test_create_evenement_post_invalid(self):
        url = reverse("create_evenement")

        data = {
            # données invalides
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("list_evenement"))

    ### READ

    def test_list_evenement(self):
        url = reverse("list_evenement")

        response = self.client.get(url)

        # Vérifie que la page fonctionne
        self.assertEqual(response.status_code, 200)

        # Vérifie le template utilisé
        self.assertTemplateUsed(
            response,
            "seance/evenement/list.html"
        )

        # Vérifie que les evenements sont présentes dans le contexte
        self.assertIn("evenements", response.context)

        # Vérifie que le evenement créé est dans la liste
        self.assertIn(
            self.evenement,
            response.context["evenements"]
        )

    
#     ### UPDATE

    def test_update_evenement_get(self):
        url = reverse(
            "update_evenement",
            kwargs={"pk": self.evenement.pk}
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "seance/evenement/update.html"
        )

        self.assertIn("form", response.context)

    def test_update_evenement_post_valid(self):
        url = reverse(
            "update_evenement",
            kwargs={"pk": self.evenement.pk}
        )
        
        # Création d'une vraie image JPEG  
        image = Image.new("RGB", (100, 100))
        
        image_io = BytesIO() 
        image.save(image_io, format="JPEG") 
        uploaded_image = SimpleUploadedFile( "1.jpg", 
        image_io.getvalue(), content_type="image/jpeg", )

        data = {
            "titre": "titre",
            "genre": "My genre",
            "description": "My description",
            "affiche": uploaded_image,       
            }

        response = self.client.post(url, data)

        # Vérifie la redirection
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse("list_evenement")
        )

        # Vérifie que le cinéma a été modifié
        self.evenement.refresh_from_db()

        self.assertEqual(
            self.evenement.titre,
            "titre"
        )


    def test_update_salle_post_invalid(self):
        url = reverse(
            "update_evenement",
            kwargs={"pk": self.evenement.pk}
        )

        # Création d'une vraie image JPEG      
        image = Image.new("RGB", (100, 100))
        
        image_io = BytesIO() 
        image.save(image_io, format="JPEG") 
        uploaded_image = SimpleUploadedFile( "1.jpg", 
        image_io.getvalue(), content_type="image/jpeg", )


        data = {
            "titre": "titre",
            "genre": "My genre",
            "description": "My description",
            "affiche": uploaded_image,       
            }

        response = self.client.post(url, data)

        # Vérifie la redirection
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse("list_evenement")
        )
        
    
    ### DELETE

    def test_delete_evenement(self):
        url = reverse(
            "delete_evenement",
            kwargs={"pk": self.evenement.pk}
        )

        response = self.client.get(url)

        # Vérifie la redirection
        self.assertEqual(response.status_code, 302)

        self.assertRedirects(
            response,
            reverse("list_evenement")
        )

        # Vérifie le message
        messages = list(response.wsgi_request._messages)

        self.assertEqual(len(messages), 1)

        self.assertEqual(
            str(messages[0]),
            "L'evenement a été supprimé"
        )

# # ------- SEANCE --------

   ### CREATE

    def test_create_seance_post_valid(self):

        url = reverse("create_seance")

        data = {
            "film": self.film.pk,
            "evenement": self.evenement.pk,
            "salle": self.salle.pk,
            "date": "2026-01-01",
            "horaire": "10h",
        }

        response = self.client.post(url, data)

        # Vérifie la redirection
        self.assertEqual(response.status_code, 302)

        self.assertRedirects(
            response,
            reverse("list_seance")
        )

        # Vérifie que la séance a été créée
        seance = Seance.objects.filter(
            salle=self.salle,
            date__date="2026-01-01",
            horaire="10h",
        ).first()

        self.assertIsNotNone(seance)

        self.assertEqual(
            seance.horaire,
            "10h"
        )

        self.assertEqual(
            seance.salle,
            self.salle
        )

        # Vérifie les valeurs calculées par la vue
        self.assertEqual(
            seance.place_dispo,
            self.salle.capacite
        )

        self.assertEqual(
            seance.programme,
            "Film"
        )

        self.assertEqual(
            seance.prix,
            5.00
        )

        # Vérifie le message
        messages = list(response.wsgi_request._messages)

        self.assertEqual(len(messages), 1)

        self.assertEqual(
            str(messages[0]),
            "La seance a été créée"
        )



    def test_create_seance_post_invalid(self):
        url = reverse("create_seance")

        data = {
            # données invalides
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("list_seance"))

#     ### READ

    def test_list_seance(self):
        url = reverse("list_seance")

        response = self.client.get(url)

        # Vérifie que la page fonctionne
        self.assertEqual(response.status_code, 200)

        # Vérifie le template utilisé
        self.assertTemplateUsed(
            response,
            "seance/seance/list.html"
        )

        # Vérifie que les seances sont présentes dans le contexte
        self.assertIn("seances", response.context)

        # Vérifie que le seance créé est dans la liste
        self.assertIn(
            self.seance,
            response.context["seances"]
        )

    
    ### UPDATE

    def test_update_seance_get(self):
        url = reverse(
            "update_seance",
            kwargs={"pk": self.seance.pk}
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "seance/seance/update.html"
        )

        self.assertIn("form", response.context)

    def test_update_seance_post_valid(self):
        url = reverse(
            "update_seance",
            kwargs={"pk": self.seance.pk}
        )
    
        data = {
                "film": self.film.pk,
                "evenement": self.evenement.pk,
                "salle": self.salle.pk,
                "date": "2026-01-01",
                "horaire": "10h",
            }     
      
   
        response = self.client.post(url, data)

        # Vérifie la redirection
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse("list_seance")
        )


        self.seance.refresh_from_db()

   
         # Vérifie que la séance a été créée
        seance = Seance.objects.filter(
            salle=self.salle,
            date__date="2026-01-01",
            horaire="10h",
        ).first()

        self.assertIsNotNone(seance)

        self.assertEqual(
            seance.horaire,
            "10h"
        )

        self.assertEqual(
            seance.salle,
            self.salle
        )
        

    def test_update_salle_post_invalid(self):
        url = reverse(
            "update_seance",
            kwargs={"pk": self.seance.pk}
        )


        data = {
            "film": self.film.pk,
            "evenement": self.evenement.pk,
            "salle": self.salle.pk,
            "date": "2026-01-01",
            "horaire": "10h",
        }     
             

        response = self.client.post(url, data)

        # Vérifie la redirection
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse("list_seance")
        )
        
    
    ## DELETE

    def test_delete_seance(self):
        url = reverse(
            "delete_seance",
            kwargs={"pk": self.seance.pk}
        )

        response = self.client.get(url)

        # Vérifie la redirection
        self.assertEqual(response.status_code, 302)

        self.assertRedirects(
            response,
            reverse("list_seance")
        )

        # Vérifie le message
        messages = list(response.wsgi_request._messages)

        self.assertEqual(len(messages), 1)

        self.assertEqual(
            str(messages[0]),
            "La seance a été supprimée"
        )