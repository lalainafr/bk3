from django.shortcuts import render
from django.http import HttpResponse    
from django.core.mail import send_mail
from django.conf import settings


def index(request):
    return render(request, "base/home.html")

def test_mail(request):
    
    send_mail(
                'titre', # titre
                "message", # message
                'settings.EMAIL_HOST_USER', # expediteur
                ['r.lalainafr2@gmail.com'], # recipient
                fail_silently=False
                )
    return HttpResponse('Email sent')
    
