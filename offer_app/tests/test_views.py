from pathlib import Path

from django.conf import settings
from django.test import Client, SimpleTestCase, TestCase
from django.urls import reverse, resolve
from offer_app import views


class TestOfferPage(TestCase, SimpleTestCase):

    def setUp(self):
        self.client = Client()

    def test_list_offer_film_uses_correct_template(self):
        response = self.client.get(reverse("list_offer_film"))
        self.assertTemplateUsed(response,  "offer/list_offer_film.html")
        
    def test_list_offer_evenement_uses_correct_template(self):
        response = self.client.get(reverse("list_offer_evenement"))
        self.assertTemplateUsed(response,  "offer/list_offer_evenement.html")
        
    def test_list_offer_film_url(self):
        url = reverse("list_offer_film")
        self.assertEqual(url, "/offer/film/")
        self.assertEqual(resolve(url).func, views.list_offer_film)
        
    def test_list_offer_evenement_url(self):
        url = reverse("list_offer_evenement")
        self.assertEqual(url, "/offer/evenement/")
        self.assertEqual(resolve(url).func, views.list_offer_evenement)

    def test_list_offer_film_contains_welcome_message_and_have_correct_status_code(self):
        response = self.client.get(reverse("list_offer_film"))
        self.assertContains(
            response,
            "Liste des films",
            status_code=200,
        )
    def test_list_offer_evenement_contains_welcome_message_and_have_correct_status_code(self):
        response = self.client.get(reverse("list_offer_evenement"))
        self.assertContains(
            response,
            "Liste des evenements",
            status_code=200,
        )



   