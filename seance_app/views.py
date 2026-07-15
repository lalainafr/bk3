from django.shortcuts import render, redirect
from .form import CreateCinemaForm, UpdateCinemaForm
from django.contrib import messages
from .models import Cinema, Salle

# ---------- CINEMA ----------


# creating cinema
def create_cinema(request):
    if request.method == 'POST':
        form = CreateCinemaForm(request.POST)
        if form.is_valid():
            var = form.save()

            messages.success(request, 'Le cinema a été créé')
            return redirect('home')
        else:
            messages.warning(request, 'Echec lors de la création du cinema')
            return redirect('home')

    else:
        form = CreateCinemaForm()
        context = {'form': form}
        return render(request, 'seance/cinema/create.html', context)

# Edit cinema
def update_cinema(request, pk):
    cinema = Cinema.objects.get(pk=pk)
    if request.method == 'POST':
        form = UpdateCinemaForm(request.POST, instance=cinema)

        if form.is_valid():
            form.save()
            messages.success(request, 'Le cinema a été modifiée')
            return redirect('list_cinema')
        else:

            messages.warning(request, {form})
            return redirect('list_cinema')

    else:
        form = UpdateCinemaForm(instance=cinema)
        context = {'form': form}
        return render(request, 'seance/cinema/update.html', context)

    
def list_cinema(request):
    cinemas = Cinema.objects.all()
    context = {'cinemas': cinemas}
    return render(request, 'seance/cinema/list.html', context)

# Delete cinema
def delete_cinema(request, pk):
    cinema = Cinema.objects.get(pk=pk)
    cinema.delete()
    return redirect('list_cinema')
