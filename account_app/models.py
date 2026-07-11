from django.db import models
from django.contrib.auth.models import AbstractUser


# create user model here
class User(AbstractUser):
    last_name = models.CharField(max_length=50, default="")
    first_name = models.CharField(max_length=50, default="")
    email = models.EmailField(unique=True)

    def __str__(self) -> str:
        return (self.last_name) + " " + self.first_name
