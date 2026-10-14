from django.db import models

from bk3.settings import AUTH_USER_MODEL
from seance_app.models import Seance

import uuid

# La seance commandée
class Order(models.Model):
    #     La séance commandée est reliée à l'utilisateur connecté
    #     Si l'utilisateur a été supprimé on supprimé la séance qu'il a commandée
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    seance = models.ForeignKey(Seance, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    # savoir si la séance été commandée
    ordered = models.BooleanField(default=False)
    subtotal = models.FloatField(default=0.00)

    def __str__(self):
        if self.seance.film:
            return f"{self.seance.programme} '{self.seance.film.titre}' le {self.seance.date.strftime('%d/%m/%Y')} à {self.seance.horaire} ({self.quantity})"
        else:
            return f"{self.seance.programme} '{self.seance.evenement.titre}' le {self.seance.date.strftime('%d/%m/%Y')} à {self.seance.horaire}  - (quantité: {self.quantity})"


# Panier
class Cart(models.Model):
    # Un utilisateur ne peut avoir qu'un seul panier
    user = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE)
    # Il peut y avoir plusieurs séances commandées dans le panier
    orders = models.ManyToManyField(Order, blank=True)
    total = models.FloatField(default=0.00)
    isPaid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}"

# Paiement
class Payment(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    birthDate = models.DateTimeField() 
    cardNumber = models.CharField(max_length=50)
    bankName = models.CharField(max_length=50)
    paymentUid =  models.UUIDField(default=uuid.uuid4)
    cartAmount = models.FloatField(default=0.00)
    orders = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return 'Paiement: '+ self.user.last_name + ' ' +  self.user.first_name + ' - ' + str(self.paymentUid)

# Ticket
class Ticket(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    payment = models.OneToOneField(Payment, on_delete=models.CASCADE, null=True, blank=True)
    qrcode = models.CharField(max_length=100)

    
    def __str__(self):
        return self.user.last_name + ' ' +  self.user.first_name  + ' ' +  str(self.payment.id) 