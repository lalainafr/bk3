from django.urls import path

from . import views

urlpatterns = [
    # cart
    path("", views.cart, name="cart"),
    path("add-to-cart-seance<str:pk>", views.add_to_cart, name="add_to_cart"),
    # Enlever un order du panier
    # path('remove-from-cart/<str:pk>', views.remove_from_cart, name='remove_from_cart'),
    path("delete/", views.delete_data, name="delete_data"),
    path("update", views.update, name="update"),
    # paiement
    path("payment", views.payment, name="payment"),
    path("valid-payment", views.valid_payment, name="valid_payment"),
    # ticket
    path("ticket-detail/<str:paymentUid>/", views.ticket_detail, name="ticket_detail"),
    path("ticket-list/", views.ticket_list, name="ticket_list"),
]
