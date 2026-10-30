from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class CinemaViewsTest(TestCase):

    def setUp(self):
        self.staff = User.objects.create_user(
            username="admin",
            password="password123",
            email="admin@test.com",
            is_staff=True,
        )

        self.normal_user = User.objects.create_user(
            username="client",
            password="password123",
            email="client@test.com",
            is_staff=False,
        )

    # ---------- TESTS DES PERMISSIONS ----------

    def test_anonymous_user_redirected_to_login(self):
        """Un utilisateur non connecté ne peut pas accéder aux vues protégées."""

        urls = [
            "create_cinema",
            "list_cinema",
            "create_salle",
            "list_salle",
            "create_film",
            "list_film",
            "create_evenement",
            "list_evenement",
            "create_seance",
            "list_seance",
        ]

        for url_name in urls:
            with self.subTest(url=url_name):
                response = self.client.get(reverse(url_name))
                self.assertEqual(response.status_code, 302)
                self.assertIn("/login", response.url)

    def test_normal_user_cannot_access_staff_views(self):
        """Un utilisateur connecté mais non staff ne peut pas accéder aux vues."""

        self.client.login(username="client", password="password123")

        urls = [
            "create_cinema",
            "list_cinema",
            "create_salle",
            "list_salle",
            "create_film",
            "list_film",
            "create_evenement",
            "list_evenement",
            "create_seance",
            "list_seance",
        ]

        for url_name in urls:
            with self.subTest(url=url_name):
                response = self.client.get(reverse(url_name))
                self.assertNotEqual(response.status_code, 200)

    # ---------- TESTS CINEMA ----------

    def test_create_cinema_get(self):
        self.client.login(username="admin", password="password123")

        response = self.client.get(reverse("create_cinema"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "seance/cinema/create.html")
        self.assertIn("form", response.context)

    def test_list_cinema_get(self):
        self.client.login(username="admin", password="password123")

        response = self.client.get(reverse("list_cinema"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "seance/cinema/list.html")
        self.assertIn("cinemas", response.context)

    # ---------- TESTS SALLE ----------

    def test_create_salle_get(self):
        self.client.login(username="admin", password="password123")

        response = self.client.get(reverse("create_salle"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "seance/salle/create.html")
        self.assertIn("form", response.context)
        self.assertIn("cinemas", response.context)

    def test_list_salle_get(self):
        self.client.login(username="admin", password="password123")

        response = self.client.get(reverse("list_salle"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "seance/salle/list.html")
        self.assertIn("salles", response.context)

    # ---------- TESTS FILM ----------

    def test_create_film_get(self):
        self.client.login(username="admin", password="password123")

        response = self.client.get(reverse("create_film"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "seance/film/create.html")
        self.assertIn("form", response.context)

    def test_list_film_get(self):
        self.client.login(username="admin", password="password123")

        response = self.client.get(reverse("list_film"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "seance/film/list.html")
        self.assertIn("films", response.context)

    # ---------- TESTS EVENEMENT ----------

    def test_create_evenement_get(self):
        self.client.login(username="admin", password="password123")

        response = self.client.get(reverse("create_evenement"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "seance/evenement/create.html")
        self.assertIn("form", response.context)

    def test_list_evenement_get(self):
        self.client.login(username="admin", password="password123")

        response = self.client.get(reverse("list_evenement"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "seance/evenement/list.html")
        self.assertIn("evenements", response.context)

    # ---------- TESTS SEANCE ----------

    def test_create_seance_get(self):
        self.client.login(username="admin", password="password123")

        response = self.client.get(reverse("create_seance"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "seance/seance/create.html")
        self.assertIn("form", response.context)
        self.assertIn("seances", response.context)

    def test_list_seance_get(self):
        self.client.login(username="admin", password="password123")

        response = self.client.get(reverse("list_seance"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "seance/seance/list.html")
        self.assertIn("seances", response.context)
