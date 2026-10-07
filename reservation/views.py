from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.http import (Http404, HttpResponse, HttpResponseBadRequest,
                         JsonResponse)
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from reservation.models import Cart, Order
from seance_app.models import Seance


def add_to_cart(request, pk):

    user = request.user

    # --> récupérer la seance concernée à partir de son id
    # s'il existe on le récupère sinon on aura une erreur 404 qui sera levée
    seance = get_object_or_404(Seance, pk=pk)

    # --> on récupére le CART (panier) appartenant à un utilisateur s'il existe, sinon on le crée en associant le panier à l'utilisateur
    # retourne 2 elements: l'objet et un boolean pour savoir s'il l'objet a été crée ou non
    cart, _ = Cart.objects.get_or_create(user=user)
    # _ convention pour une variable qui ne sera pas utilisée par la suite (ca ne nous interesse pas de savoir si le panier existe ou non)
    # --> la seance sera créer qu'une seule fois dans le panier

    # si la seance existe dans le pânier de la bdd on l'incremente sinon on le créer et le rajoute dans le panier
    # On récupère ORDER qui est associée à un user et qui correspont à la séance concernée
    order, created = Order.objects.get_or_create(user=user, seance=seance)
    # order: l'objet
    # created: bool pour savoir si l'element a été crée ou non

    # On incremente la quantité si la seance existe
    if not created:
        order.quantity += 1
        order.save()

    # cela veut dire qu'il n'existe pas encore dans le panier, donc il faudra le créer (avec l'element qu'on a récupérer: 'order')
    cart.orders.add(order)
    order.subtotal = order.seance.prix * order.quantity
    order.ordered = True
    order.save()

    cart.total = sum(order.subtotal for order in cart.orders.all())
    cart.save()

    if order.seance.film:
        return redirect(reverse("list_offer_film"))
    else:
        return redirect(reverse("list_offer_evenement"))


def cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)

    orders = cart.orders.all()

    return render(
        request,
        "reservation/cart.html",
        {
            "cart": cart,
            "orders": orders,
        },
    )


# supprimer un order dans le panier
# def remove_from_cart(request, pk):
#     order = Order.objects.get(pk=pk)
#     order.delete()
#     return redirect('cart')


# AJAX - supprimer un order dans le panier
@csrf_exempt
def delete_data(request):
    # requete POST à partir de l'AJAX
    if request.method == "POST":
        id = request.POST.get("order_id")

        order = Order.objects.get(pk=id)
        cart = Cart.objects.get(user=request.user)

        order.delete()

        # on actualise la valeur du TOTAL après la suppression d'un order
        cart.total = sum(order.subtotal for order in cart.orders.all())

        cart.save()

        return JsonResponse(
            {
                "status": 1,
                "total": cart.total,
                "order_count": cart.orders.count(),
                "subtotal": order.subtotal,
            }
        )

    return JsonResponse({"status": 0})


# From to procces the data for update order quantity
class UpdateForm(forms.Form):
    operation = forms.CharField()
    id = forms.IntegerField()


# ajax update order quantity
def update(request):
    if request.method != "POST":
        return HttpResponseBadRequest("invalid method")

    form = UpdateForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest()

    data = form.cleaned_data
    print(data)

    # Avec "select_for_update()" , le verrou permet d'éviter que les deux requêtes travaillent sur la même ancienne valeur de manière incorrecte.

    with transaction.atomic():

        # Gerer  l'exception si order n'existe pas
        try:

            # Récuperer order
            obj = Order.objects.select_for_update().get(pk=data["id"])

            # Incremente sa quantité si on appuye sur add sinon on le décremente
            obj.quantity += 1 if data["operation"] == "add" else -1

            # Pas de valeur négative pour la quantité
            # en dessous de 1 la quantité le bouge plus - on doit appuyer sur delete pour supprier l'article dans le panier
            if obj.quantity < 1:
                obj.quantity = 1

            # Modifier la quantité de order dans la base de données
            obj.subtotal = obj.quantity * obj.seance.prix
            obj.save()

            # Retrouver le panier qui contient cette commande
            cart = Cart.objects.get(orders=obj)

            # Récupérer toutes les commandes du panier
            orders = cart.orders.all()

            # Calculer le total
            total = sum(order.subtotal for order in orders)

            # Sauvegarder le total
            cart.total = total
            cart.save()

            return HttpResponse(str(obj.quantity))
        except ObjectDoesNotExist:
            raise Http404("not found")
    return HttpResponse("ok")
