from django.shortcuts import render, redirect
from datetime import datetime, timedelta
from collections import defaultdict
from django.utils import timezone
from seance_app.views import Seance


def list_offer_film(request):
    seances = Seance.objects.all()
    context = {'seances': seances}
    return render(request, "offer/list_offer_film.html", context)

def list_offer_evenement(request):
    seances = Seance.objects.all()
    context = {'seances': seances}
    return render(request, "offer/list_offer_evenement.html", context)

# def detail_dispo(request):

#     semaine = request.GET.get("week")

#     if semaine:
#         lundi = datetime.strptime(semaine, "%Y-%m-%d").date()
#     else:
#         lundi = timezone.localdate()
#         lundi -= timedelta(days=lundi.weekday())

#     dimanche = lundi + timedelta(days=6)

#     disponibilites = Seance.objects.filter(
#         date__range=[lundi, dimanche]
#     )

#     jours = defaultdict(list)

#     for s in disponibilites:
#         jours[s.date].append(s)

#     semaine_data = []

#     for i in range(7):

#         jour = lundi + timedelta(days=i)

#         semaine_data.append({
#             "date": jour,
#             "creneaux": jours[jour]
#         })

#     context = {
#         "semaine": semaine_data,
#         "precedente": lundi - timedelta(days=7),
#         "suivante": lundi + timedelta(days=7),
#     }

#     # Si la requête vient de HTMX
#     if request.headers.get("HX-Request"):
#         return render(request, "seance/_calendrier.html", context)

#     return render(request, "seance/calendrier.html", context)