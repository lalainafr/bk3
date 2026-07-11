from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class TestSignIn(TestCase):

    def test_register_user_success(self):
        response = self.client.post(
            reverse("register_user"),
            {
                "first_name": "myFirstname",
                "last_name": "myLastname",
                "email": "myUser@mail.mail",
                "password1": "myStrongPassword123!",
                "password2": "myStrongPassword123!",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="myUser@mail.mail").exists())
        # username equals email in the account.view.register_user

    def test_register_user_success_message(self):
        response = self.client.post(
            reverse("register_user"),
            {
                "first_name": "myFirstname",
                "last_name": "myLastname",
                "email": "myUser@mail.mail",
                "password1": "myStrongPassword123!",
                "password2": "myStrongPassword123!",
            },
        )

        response = self.client.post(reverse("register_user"), follow=True)
        self.assertContains(response, "User created")

    def test_register_user_fail_message(self):
        response = self.client.post(
            reverse("register_user"),
            {
                "first_name": "myFirstname",
                "last_name": "myLastname",
                "email": "myUser@mail.mail",
                "password1": "myStrongPassword123!",
                "password2": "notMyStrongPassword123!",
            },
        )

        response = self.client.get(reverse("register_user"))
        self.assertContains(response, "Something went wrong")


class TestLogin(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="myUser", password="myPassword")

    def test_successful_login(self):
        log_user = self.client.login(username="myUser", password="myPassword")

        self.assertTrue(log_user)
        response = self.client.post(reverse("login"), follow=True)
        self.assertTrue(response.context["user"].is_authenticated)

    def test_failed_login(self):
        log_user = self.client.login(username="myUser", password="notMyPassword")

        self.assertFalse(log_user)
        response = self.client.post(reverse("login"), follow=True)
        self.assertFalse(response.context["user"].is_authenticated)


class TestLogout(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="myUser", password="myPassword")

    def test_logout(self):
        self.client.login(username="myUser", password="myPassword")

        response = self.client.post(reverse("logout"), follow=True)
        self.assertFalse(response.context["user"].is_authenticated)

    def test_logout_message(self):
        self.client.login(username="myUser", password="myPassword")

        response = self.client.post(reverse("logout"), follow=True)
        self.assertContains(response, "You have been logged out", status_code=200)
