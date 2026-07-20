from django.test import TestCase, Client, SimpleTestCase
from django.urls import reverse
from pathlib import Path
from django.conf import settings


class TestHomePage(TestCase, SimpleTestCase):

    def setUp(self):
        self.client = Client()

    def test_homepage_uses_correct_template(self):
        response = self.client.get(reverse("home"))
        self.assertTemplateUsed(response, "base_app/index.html")

    def test_homepage_contains_welcome_message_and_have_correct_status_code(self):
        response = self.client.get(reverse("home"))
        self.assertContains(
            response,
            "Neque porro quisquam est qui dolorem ipsum quia dolor sit amet",
            status_code=200,
        )

    def test_homepage_with_correct_title(self):
        response = self.client.get(reverse("home"))
        self.assertContains(
            response, "<title>Portfolio for bachelor exam</title>", html=True
        )

    def test_homepage_contains_company_logo(self):
        logo_path = Path(settings.BASE_DIR) / "staticfiles" / "img" / "logo1.jpg"
        self.assertTrue(logo_path.exists(), f"expected logo image at {logo_path}")
