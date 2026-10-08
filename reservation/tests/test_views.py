from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.test import TestCase
from django.urls import reverse

User = get_user_model()

from decimal import Decimal

from reservation.models import Cart, Order
from seance_app.models import Cinema, Evenement, Film, Salle, Seance


class TestCart(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )

        self.client.login(username="testuser", password="password123")

        self.cart = Cart.objects.create(user=self.user, total=0)

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

        self.evenement = Evenement.objects.create(
            titre="titre",
            description="description",
            genre="genre",
            affiche="evenements/1.jpg",
        )

        self.film = Film.objects.create(
            titre="titre",
            duree=4,
            genre="genre",
            date_sortie="2026-01-02",
            realisateur="realisateur",
            description="description",
            affiche="films/2.jpg",
        )

        self.seance = Seance.objects.create(
            film=self.film,
            evenement=None,
            programme="programme",
            place_dispo=1,
            salle=self.salle,
            date_created="2026-01-02",
            date="2026-01-02",
            horaire="11h",
            prix=Decimal("5.00"),
        )

    # ADD CART
    def test_add_to_cart(self):
        response = self.client.get(reverse("add_to_cart", args=[self.seance.pk]))
        # Verifie la redirection
        self.assertEqual(response.status_code, 302)

        # Verifie que le panier existe
        cart = Cart.objects.get(user=self.user)

        # Verifie que la commande a été créé
        order = Order.objects.get(user=self.user, seance=self.seance)

        # Vérifie la quantité
        self.assertEqual(order.quantity, 1)

        # Vérifie le sous-total
        self.assertEqual(order.subtotal, 5.00)

        # Vérifie que l'order a été commandée
        self.assertTrue(order.ordered)

        # Verifie que l'order est dans le panier
        self.assertEqual(cart.orders.count(), 1)

        # Verifie le total du panier
        self.assertEqual(cart.total, 5.00)

    # TEST CAS D'ERREUR
    def test_add_unknown_seance(self):
        response = self.client.get(
            # teste de cas d'erreur avec l'id d'une seance inexsitante
            reverse("add_to_cart", args=[999999])
        )

        self.assertEqual(response.status_code, 404)

    # DELETE DATA
    def test_delete_data(self):
        # Création d'une commande uniquement pour ce test
        self.order = Order.objects.create(
            user=self.user, seance=self.seance, quantity=1, ordered=True, subtotal=5.00
        )

        # Ajout de la commande au panier
        self.cart.orders.add(self.order)

        # Mise à jour du total du panier
        self.cart.total = 5.00
        self.cart.save()

        # Requête POST
        response = self.client.post(reverse("delete_data"), {"order_id": self.order.id})

        # Vérifie la réponse
        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertEqual(data["status"], 1)

        self.assertEqual(data["total"], 0)

        self.assertEqual(data["order_count"], 0)

        self.assertEqual(data["subtotal"], 5.00)

        # Vérifie que l'Order a été supprimé
        self.assertFalse(Order.objects.filter(pk=self.order.id).exists())

        # Vérifie que le panier est vide
        self.cart.refresh_from_db()

        self.assertEqual(self.cart.total, 0)

    # UPDATE
    # Augmenter la quantité
    def test_update_add(self):

        # Création d'une commande
        self.order = Order.objects.create(
            user=self.user,
            seance=self.seance,
            quantity=1,
            ordered=True,
            subtotal=5.00,
        )

        # Ajout commande dans le panier de l'utilisateur
        self.cart.orders.add(self.order)

        # Envoi requete POST afin d'incrementer la quantité
        response = self.client.post(
            reverse("update"),
            {
                "operation": "add",
                "id": self.order.id,
            },
        )

        # Vérifier si la requete http à été réussie
        self.assertEqual(response.status_code, 200)

        # La vue retourne la nouvelle quantité
        self.assertEqual(response.content.decode(), "2")

        # Recharge order depuis la base de données afin de récupérer les valeurs réellement enregistrées
        self.order.refresh_from_db()

        # Vérifier si la quantité est bien passé de 1 à 2
        self.assertEqual(self.order.quantity, 2)

        # Vérifier si le sous total est bien passé à 10 (2 * 5)
        self.assertEqual(self.order.subtotal, 10.00)

        # Recharge le panier depuis la base de données
        self.cart.refresh_from_db()

        # Vérifier si le total du panier à été reclaculé
        self.assertEqual(self.cart.total, 10.00)

    # REMOVE
    # Diminuer la quantité d'une commande
    def test_update_remove(self):

        # Création d'une commande
        self.order = Order.objects.create(
            user=self.user,
            seance=self.seance,
            quantity=1,
            ordered=True,
            subtotal=5.00,
        )

        # Ajout commande dans le panier de l'utilisateur
        self.cart.orders.add(self.order)

        # On commence par une quantité de 2 pour tester la diminution de la quantité de la commande
        self.order.quantity = 2

        # Calcul du nouveau sous-total
        self.order.subtotal = 10.00

        # Enregistre les modifications dans la base de données
        self.order.save()

        # Le panier contient actuellement 10.00
        self.cart.total = 10.00
        self.cart.save()

        # Envoi requete POST vafin d'incrementer la quantité
        response = self.client.post(
            reverse("update"),
            {
                "operation": "remove",
                "id": self.order.id,
            },
        )

        # Vérifier si la requete http à été réussie
        self.assertEqual(response.status_code, 200)

        # La vue doit passer de '2' à '1'
        self.assertEqual(response.content.decode(), "1")

        # Recharge order depuis la base de données afin de récupérer les valeurs réellement enregistrées
        self.order.refresh_from_db()

        # Vérifier si la quantité est bien passé de 2 à 1
        self.assertEqual(self.order.quantity, 1)

        # vérifie nouveau sous-total (5*1)
        self.assertEqual(self.order.subtotal, 5.00)

        # Recharge le panier depuis la base de données
        self.cart.refresh_from_db()

        # Vérifie que le total est passé à 5
        self.assertEqual(self.cart.total, 5.00)

    # REMOVE - la quantité ne peut pas descendre en dessous de 1
    def test_update_remove_quantity_cannot_go_below_one(self):

        # Création d'une commande
        self.order = Order.objects.create(
            user=self.user,
            seance=self.seance,
            quantity=1,
            ordered=True,
            subtotal=5.00,
        )

        # Ajout commande dans le panier de l'utilisateur
        self.cart.orders.add(self.order)

        # Envoie un requete afin de diminuer la quantité, alors que la quantité est déjà à 1
        response = self.client.post(
            reverse("update"),
            {
                "operation": "remove",
                "id": self.order.id,
            },
        )

        # Vérifier si la requete a réussi
        self.assertEqual(response.status_code, 200)

        # La quantité doi rester à 1, et ne doit jamais décendre en dessous de 1 (0 ou négatif)
        self.assertEqual(response.content.decode(), "1")

        # Recharg Order depuis la base de données
        self.order.refresh_from_db()

        # Vérifie que la quantité reste toujours égal à 1
        self.assertEqual(self.order.quantity, 1)

        # Vérifier que le sous total reste à 5
        self.assertEqual(self.order.subtotal, 5.00)

    #  METHODE INVALIDE
    def test_update_invalid_method(self):

        # Envoie d'une requette GET alors que la vue accepte seulement les requetes POST
        response = self.client.get(reverse("update"))

        # Retourne une erreur 404
        self.assertEqual(response.status_code, 400)

    # FROMULAIRE INVALIDE
    def test_update_invalid_form(self):

        # Vérifier l'envoi d'une requete POST incomplète (champ 'id' manquant)
        response = self.client.post(reverse("update"), {"operation": "add"})
        # Formulaire invalide , lavue retourn une erreur 404
        self.assertEqual(response.status_code, 400)

    # ORDER NON TROUVE
    def test_update_order_not_found(self):

        # vérifier l'envoi d'un requete avce un ID de commande qui n'existe pas dans la base de données
        response = self.client.post(
            reverse("update"),
            {
                "operation": "add",
                "id": 999999,
            },
        )

        # La vue doit lever une erreur 404
        self.assertEqual(response.status_code, 404)
