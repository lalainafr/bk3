from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("mail/", views.test_mail, name="test_mail"),
]
