from django.test import TestCase, Client, SimpleTestCase
from django.urls import reverse
from pathlib import Path
from django.conf import settings

class TestHomePage(TestCase, SimpleTestCase):
    
    def setUp(self):
        self.client = Client()
    
    def test_homepage_uses_correct_template(self):
        response = self.client.get(reverse("index"))
        self.assertTemplateUsed(response, 'base_app/index.html')
    
    def test_homepage_contains_welcome_message_and_have_correct_status_code(self):
        response = self.client.get(reverse("index"))
        self.assertContains(response, 'The car of your dream is waiting for you', status_code=200)
    
    def test_homepage_with_correct_title(self):
        response = self.client.get(reverse("index"))
        self.assertContains(response, "<title>Web site do serve as a portfolio</title>", html=True)
        
    def test_homepage_contains_company_logo(self):
        logo_path =  Path(settings.BASE_DIR)/"staticfiles"/"img"/"logo.png"
        self.assertTrue(logo_path.exists(), f"expected logo image at {logo_path}")