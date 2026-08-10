from django.shortcuts import render
from django.http import HttpResponse    
from django.core.mail import send_mail
from django.conf import settings


def index(request):
    return render(request, "base/home.html")

def test_mail(request):
    
    send_mail(
                'Tester Un autre titre', # titre
                " Tester Un autre message", # message
                settings.DEFAULT_FROM_EMAIL, # expediteur
                ['r.lalainafr@gmail.com'], # recipient
                fail_silently=False
                )
    return HttpResponse('Email sent')
    
