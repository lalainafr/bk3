from django.shortcuts import render, redirect, get_object_or_404
from seance_app.models import Seance
from reservation.models import Cart, Order
from django.urls import reverse
from django.utils import timezone
from django.http import JsonResponse

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
    order, created = Order.objects.get_or_create(user=user, seance = seance)
    # order: l'objet
    # created: bool pour savoir si l'element a été crée ou non

    if created:
    # cela veut dire qu'il n'existe pas encore dans le panier, donc il faudra le créer (avec l'element qu'on a récupérer: 'order')   
        cart.orders.add(order)
        order.ordered = True
        order.ordered_date = timezone.now()
        order.save()
        cart.save()   
            
    else:
        order.quantity += 1
        order.save()  
    if order.seance.film:
        return redirect(reverse("list_offer_film"))
    else:
        return redirect(reverse("list_offer_evenement"))
        
            

def cart(request):
    cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    orders = cart.orders.all()

    return render(
        request,
        "reservation/cart.html",
        {
            "cart": cart,
            "orders": orders,
        }
    )

# supprimer un order dans le panier
def remove_from_cart(request, pk):
    order = Order.objects.get(pk=pk)
    order.delete()
    return redirect('cart')
    
    