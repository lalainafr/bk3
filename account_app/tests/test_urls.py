from django.test import SimpleTestCase
from django.urls import resolve, reverse

from account_app import views

  
class AccountUrlsTest(SimpleTestCase):

    def test_register_user_url(self):
        url = reverse("register_user")
        self.assertEqual(url, "/register-user/")
        self.assertEqual(resolve(url).func, views.register_user)

    def test_login_url(self):
        url = reverse("login")
        self.assertEqual(url, "/login/")
        self.assertEqual(resolve(url).func, views.login_user)

    def test_logout_url(self):
        url = reverse("logout")
        self.assertEqual(url, "/logout/")
        self.assertEqual(resolve(url).func, views.logout_user)

   