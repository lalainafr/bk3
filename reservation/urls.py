from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart, name="cart"),
    path('delete/', views.delete_cart, name="delete_cart"),
    path('add-to-cart-seance<str:pk>', views.add_to_cart, name="add_to_cart"),

]