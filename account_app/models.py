import random
from datetime import timedelta
from random import choice, randint

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


# create user model here
class User(AbstractUser):
    last_name = models.CharField(max_length=50, default="")
    first_name = models.CharField(max_length=50, default="")
    email = models.EmailField(unique=True)

    def __str__(self) -> str:
        return self.username


# A chaque user crée, données random assignées
def random_birthday():
    # on récupére al date actuelle
    today = timezone.now()
    # donne un nombre aléatoire entre A et B
    days = random.randint(18 * 365, 80 * 365)
    return today - timedelta(days=days)


def random_bank():
    return choice(["Bred", "Banque postale", "Caisse d'epargne", "BNP Paribas"])


def random_account_number():
    return str(randint(10000000000, 99999999999))


def random_balance():
    return randint(100, 10000)


class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)

    # les informations suivantes servent pour la 'SIMULATION DE PAIEMENT' --> elles seront renvoyées sous forme JSON et seront appellées à partir d'un end point afin de vérifier les informations du paiement d'un user
    birthday = models.DateTimeField(default=random_birthday)
    bankName = models.CharField(max_length=50, default=random_bank)
    accountNb = models.CharField(max_length=50, default=random_account_number)
    accountBalance = models.FloatField(default=random_balance)

    def __str__(self) -> str:
        return f"Profil de {self.user.username}"
