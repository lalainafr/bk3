from django.shortcuts import render, redirect
from seance_app.views import Seance
from collections import defaultdict



def list_offer_film(request):
    seances = Seance.objects.select_related("film").order_by("film","date","horaire")
    
    # On créer une liste
    films = defaultdict(list)
    
    # On rajoute les films dans les  séances dans la liste
    for seance in seances:
        if seance.programme == 'Film':
            films[seance.film].append(seance)
            prix = seance.prix
        
    context = {'films': films.items(), 'prix': prix}
    return render(request, "offer/list_offer_film.html", context)

def list_offer_evenement(request):
    seances = Seance.objects.select_related("evenement").order_by("evenement","date","horaire")
    
    # On créer une liste
    evenements = defaultdict(list)
    
    # On rajoute les films dans les  séances dans la liste
    for seance in seances:
        if seance.programme == 'Evenement':
            evenements[seance.evenement].append(seance)
            prix = seance.prix
            
    context = {'evenements': evenements.items(), 'prix': prix}
    return render(request, "offer/list_offer_evenement.html", context)

