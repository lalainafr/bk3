from pathlib import Path

from django.conf import settings
from django.test import Client, SimpleTestCase, TestCase
from django.urls import reverse, resolve
from base_app import views


class TestHomePage(TestCase, SimpleTestCase):

    def setUp(self):
        self.client = Client()

    def test_homepage_uses_correct_template(self):
        response = self.client.get(reverse("home"))
        self.assertTemplateUsed(response, "base/home.html")

    def test_homepage_contains_welcome_message_and_have_correct_status_code(self):
        response = self.client.get(reverse("home"))
        self.assertContains(
            response,
            "Neque porro quisquam",
            status_code=200,
        )

    def test_homepage_contains_company_logo(self):
        logo_path = Path(settings.BASE_DIR) / "staticfiles" / "img" / "image.png"
        self.assertTrue(logo_path.exists(), f"expected logo image at {logo_path}")

    def test_home_url(self):
            url = reverse("home")
            self.assertEqual(url, "/")
            self.assertEqual(resolve(url).func, views.index)