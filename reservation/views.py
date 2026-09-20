from django.shortcuts import render, redirect

from django.contrib import messages
from . models import  Seance

# # List seance par film
# def list_seance_par_film(request, film):
#     seances = Seance.objects.filter(film_id = film.id)
#     context = {"seances": seances}
#     return render(request, "reservation/listSeanceParFilm.html", context)

