from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart, name="cart"),

    path('add-to-cart-seance<str:pk>', views.add_to_cart, name="add_to_cart"),

    # Enlever un order du panier 
    # path('remove-from-cart/<str:pk>', views.remove_from_cart, name='remove_from_cart'),
    path('delete/', views.delete_data, name='delete_data'),
    
    path('update', views.update, name='update'),
]