from django.shortcuts import render, redirect
from seance_app.views import Seance, Film, Evenement
from collections import defaultdict



def list_offer_film(request):
    seances = Seance.objects.select_related("film").order_by("film","date","horaire")
    
    prix=0
    
    # On créer une liste
    films = defaultdict(list)
    
    # On rajoute les films dans les  séances dans la liste
    for seance in seances:
        if seance.programme == 'Film':
            films[seance.film].append(seance)
            prix = seance.prix
        
    context = {'films': films.items(), 'prix': prix}
    return render(request, "offer/offer_film.html", context)

def list_offer_evenement(request):
    seances = Seance.objects.select_related("evenement").order_by("evenement","date","horaire")
    
    prix=0
    
    # On créer une liste
    evenements = defaultdict(list)
    
    # On rajoute les films dans les  séances dans la liste
    for seance in seances:
        if seance.programme == 'Evenement':
            evenements[seance.evenement].append(seance)
            prix = seance.prix
            
    context = {'evenements': evenements.items(), 'prix': prix}
    return render(request, "offer/offer_evenement.html", context)


# Choix créneau du film
def creneau_film(request, pk):
    film = Film.objects.get(pk=pk)
    seances = Seance.objects.filter(film = film)
    context = {"seances": seances,
               "film": film,}
    return render(request, "offer/creneau_film.html", context)

# Choix creneau de l'evenement
def creneau_evenement(request, pk):
    evenement = Evenement.objects.get(pk=pk)
    seances = Seance.objects.filter(evenement = evenement)
    context = {"seances": seances,
               "evenement": evenement,}
    return render(request, "offer/creneau_evenement.html", context)

