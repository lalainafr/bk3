# views.py
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Sum
from django.shortcuts import render

from reservation.models import Ticket
from seance_app.models import Seance


@login_required(login_url="login")
@user_passes_test(lambda user: user.is_staff)
def main_dashboard(request):
    return render(request, "dashboard/main_dashboard.html")


@login_required(login_url="login")
@user_passes_test(lambda user: user.is_staff)
def dashboard_remplissage_seance(request):
    seances = Seance.objects.select_related(
        "salle", "salle__cinema", "film", "evenement"
    )

    resultats = []

    for seance in seances:
        capacite = seance.salle.capacite
        disponibles = seance.place_dispo

        if capacite > 0 and disponibles is not None:
            taux = round((capacite - disponibles) / capacite * 100, 1)
        else:
            taux = None

        resultats.append(
            {
                "seance": seance,
                "capacite": capacite,
                "disponibles": disponibles,
                "taux": taux,
            }
        )

        print(seance.evenement)

    return render(
        request,
        "dashboard/remplissage_seance.html",
        {"resultats": resultats},
    )


@login_required(login_url="login")
@user_passes_test(lambda user: user.is_staff)
def dashboard_remplissage_salle(request):
    seances = Seance.objects.select_related(
        "salle", "salle__cinema", "film", "evenement"
    )

    salles_dict = {}

    for seance in seances:
        salle = seance.salle
        capacite = salle.capacite
        disponibles = seance.place_dispo

        salle_id = salle.id

        if salle_id not in salles_dict:
            salles_dict[salle_id] = {
                "salle": salle,
                "capacite": capacite,
                "total_disponibles": 0,
                "nb_seances": 0,
            }

        if disponibles is not None:
            salles_dict[salle_id]["total_disponibles"] += disponibles
            salles_dict[salle_id]["nb_seances"] += 1

    resultats = []

    for data in salles_dict.values():
        capacite = data["capacite"]
        disponibles = data["total_disponibles"]
        nb_seances = data["nb_seances"]

        # Capacité totale pour toutes les séances
        capacite_totale = capacite * nb_seances

        if capacite_totale > 0:
            taux = round(
                (capacite_totale - disponibles) / capacite_totale * 100,
                1,
            )
        else:
            taux = None

        resultats.append(
            {
                "salle": data["salle"],
                "capacite": capacite_totale,
                "disponibles": disponibles,
                "nb_seances": nb_seances,
                "taux": taux,
            }
        )

    return render(
        request,
        "dashboard/remplissage_salle.html",
        {"resultats": resultats},
    )


@login_required(login_url="login")
@user_passes_test(lambda user: user.is_staff)
def dashboard_remplissage_creneau(request):
    creneaux = ["10h", "14h", "17h", "21h"]
    resultats = []

    for creneau in creneaux:
        seances = Seance.objects.filter(horaire=creneau)

        donnees = seances.aggregate(
            capacite_totale=Sum("salle__capacite"),
            places_disponibles=Sum("place_dispo"),
        )

        capacite = donnees["capacite_totale"] or 0
        disponibles = donnees["places_disponibles"] or 0

        occupees = max(0, capacite - disponibles)

        taux = round(occupees / capacite * 100, 2) if capacite > 0 else 0

        resultats.append(
            {
                "horaire": creneau,
                "capacite": capacite,
                "places_disponibles": disponibles,
                "places_occupees": occupees,
                "taux": taux,
            }
        )

    return render(
        request,
        "dashboard/remplissage_creneau.html",
        {"resultats": resultats},
    )


# Liste des tickets de tous les utilisateurs
@login_required(login_url="login")
@user_passes_test(lambda user: user.is_staff)
def all_ticket_list(request):
    tickets = Ticket.objects.all()

    for ticket in tickets:
        ticket.orders_formatted = (
            str(ticket.payment.orders)
            .replace(", <Order:", "\n<Order:")
            .replace("[", "")
            .replace("<", "-")
            .replace(">", "")
            .replace("]", "")
            .replace("Order:", "")
        )

    context = {"tickets": tickets}
    return render(request, "dashboard/all_ticket_list.html", context)
