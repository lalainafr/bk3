from django.shortcuts import render, redirect
from .form import (
    CreateCinemaForm,
    UpdateCinemaForm,
    CreateSalleForm,
    UpdateSalleForm,
    CreateFilmForm,
    UpdateFilmForm,
    CreateEvenementForm,
    UpdateSeanceForm,
    CreateSeanceForm,
    UpdateEvenementForm,
)
from django.contrib import messages
from .models import Cinema, Salle, Film, Evenement, Seance

# ---------- CINEMA ----------


# creating cinema
def create_cinema(request):
    if request.method == "POST":
        form = CreateCinemaForm(request.POST)
        if form.is_valid():
            form.save()

            messages.success(request, "Le cinema a été créé")
            return redirect("list_cinema")
        else:
            messages.warning(request, "Echec lors de la création du cinema")
            return redirect("list_cinema")

    else:
        form = CreateCinemaForm()
        context = {"form": form}
        return render(request, "seance/cinema/create.html", context)


# Edit cinema
def update_cinema(request, pk):
    cinema = Cinema.objects.get(pk=pk)
    if request.method == "POST":
        form = UpdateCinemaForm(request.POST, instance=cinema)

        if form.is_valid():
            form.save()
            messages.success(request, "Le cinema a été modifiée")
            return redirect("list_cinema")
        else:
            messages.warning(request, {form})
            return redirect("list_cinema")
    else:
        form = UpdateCinemaForm(instance=cinema)
        context = {"form": form}
        return render(request, "seance/cinema/update.html", context)


# List cinema
def list_cinema(request):
    cinemas = Cinema.objects.all()
    context = {"cinemas": cinemas}
    return render(request, "seance/cinema/list.html", context)


# Delete cinema
def delete_cinema(request, pk):
    cinema = Cinema.objects.get(pk=pk)
    cinema.delete()
    messages.success(request, "Le cinema a été supprimé")
    return redirect("list_cinema")


# ---------- SALLE ----------


# creating salle
def create_salle(request):
    if request.method == "POST":
        form = CreateSalleForm(request.POST)
        if form.is_valid():
            form.save()

            messages.success(request, "La salle a été créée")
            return redirect("list_salle")
        else:
            messages.warning(request, "Echec lors de la création de la salle")
            return redirect("list_salle")

    else:
        form = CreateSalleForm()
        cinemas = Cinema.objects.all()
        context = {"form": form, "cinemas": cinemas}
        return render(request, "seance/salle/create.html", context)


# Edit salle
def update_salle(request, pk):
    salle = Salle.objects.get(pk=pk)
    if request.method == "POST":
        form = UpdateSalleForm(request.POST, instance=salle)

        if form.is_valid():
            form.save()
            messages.success(request, "Le salle a été modifiée")
            return redirect("list_salle")
        else:

            messages.warning(request, {form})
            return redirect("list_salle")

    else:
        form = UpdateSalleForm(instance=salle)
        context = {"form": form}
        return render(request, "seance/salle/update.html", context)


# Delete salle
def list_salle(request):
    salles = Salle.objects.all()
    context = {"salles": salles}
    return render(request, "seance/salle/list.html", context)


# Delete salle
def delete_salle(request, pk):
    salle = Salle.objects.get(pk=pk)
    salle.delete()
    messages.success(request, "La salle a été supprimée")
    return redirect("list_salle")


# ---------- FILM ----------


# creating film
def create_film(request):
    if request.method == "POST":
        form = CreateFilmForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

            messages.success(request, "Le film a été créé")
            return redirect("list_film")
        else:
            messages.warning(request, "Echec lors de la création du film")
            return redirect("list_film")

    else:
        form = CreateFilmForm()
        context = {"form": form}
        return render(request, "seance/film/create.html", context)


# Edit film
def update_film(request, pk):
    film = Film.objects.get(pk=pk)
    if request.method == "POST":
        form = UpdateFilmForm(request.POST, request.FILES, instance=film)

        if form.is_valid():
            form.save()
            messages.success(request, "Le film a été modifiée")
            return redirect("list_film")
        else:

            messages.warning(request, {form})
            return redirect("list_film")

    else:
        form = UpdateFilmForm(instance=film)
        context = {"form": form}
        return render(request, "seance/film/update.html", context)


# List film
def list_film(request):
    films = Film.objects.all()
    context = {"films": films}
    return render(request, "seance/film/list.html", context)


# Detail film
def detail_film(request, pk):
    film = Film.objects.get(pk=pk)
    context = {"film": film}
    return render(request, "seance/film/details.html", context)


# Delete film
def delete_film(request, pk):
    film = Film.objects.get(pk=pk)
    film.delete()
    messages.success(request, "Le film a été supprimé")
    return redirect("list_film")


# ---------- EVENEMENT ----------


# creating evenement
def create_evenement(request):
    if request.method == "POST":
        form = CreateEvenementForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

            messages.success(request, "L'evenement a été créé")
            return redirect("list_evenement")
        else:
            messages.warning(request, "Echec lors de la création de l'evenement")
            return redirect("list_evenement")

    else:
        form = CreateEvenementForm()
        context = {"form": form}
        return render(request, "seance/evenement/create.html", context)


# Edit evenement
def update_evenement(request, pk):
    evenement = Evenement.objects.get(pk=pk)
    if request.method == "POST":
        form = UpdateEvenementForm(request.POST, request.FILES, instance=evenement)

        if form.is_valid():
            form.save()
            messages.success(request, " L'evenement a été modifiée")
            return redirect("list_evenement")
        else:

            messages.warning(request, {form})
            return redirect("list_evenement")

    else:
        form = UpdateEvenementForm(instance=evenement)
        context = {"form": form}
        return render(request, "seance/evenement/update.html", context)


# List evenement
def list_evenement(request):
    evenements = Evenement.objects.all()
    context = {"evenements": evenements}
    return render(request, "seance/evenement/list.html", context)


# Delete evenement
def delete_evenement(request, pk):
    evenement = Evenement.objects.get(pk=pk)
    evenement.delete()
    messages.success(request, "L'evenement a été supprimé")
    return redirect("list_evenement")


# ---------- SEANCE ----------


# creating seance
def create_seance(request):
    if request.method == "POST":
        form = CreateSeanceForm(request.POST)
        if form.is_valid():
            var = form.save(commit=False)
            var.place_dispo = var.salle.capacite
            if var.film:
                var.programme = "Film"
                var.prix = 5.00
            else:
                var.programme = "Evenement"
                var.prix = 9.99
            var.save()

            messages.success(request, "La seance a été créée")
            return redirect("list_seance")
        else:
            print(form)
            messages.warning(request, "Echec lors de la création de la seance")
            return redirect("list_seance")

    else:
        form = CreateSeanceForm()
        seances = Seance.objects.all()
        context = {"form": form, "seances": seances}
        return render(request, "seance/seance/create.html", context)


# Edit seance
def update_seance(request, pk):
    seance = Seance.objects.get(pk=pk)
    if request.method == "POST":
        form = UpdateSeanceForm(request.POST, instance=seance)
        if form.is_valid():
            var = form.save(commit=False)
            var.place_dispo = var.salle.capacite
            if var.film:
                var.programme = "Film"
                var.prix = 5.00
            else:
                var.programme = "Evenement"
                var.prix = 9.99
            var.save()
            messages.success(request, "La séance a été modifiée")
            return redirect("list_seance")
        else:

            messages.warning(request, {form})
            return redirect("list_seance")

    else:
        form = UpdateSeanceForm(instance=seance)
        context = {"form": form}
        return render(request, "seance/seance/update.html", context)


# List seance
def list_seance(request):
    seances = Seance.objects.all()
    context = {"seances": seances}
    return render(request, "seance/seance/list.html", context)


# Delete seance
def delete_seance(request, pk):
    seance = Seance.objects.get(pk=pk)
    seance.delete()
    messages.success(request, "La salle a été supprimée")
    return redirect("list_seance")
