from django.db import models
from bk3.settings import AUTH_USER_MODEL
from seance_app.models import Seance

# La seance commandée
class Order(models.Model):
#     La séance commandée est reliée à l'utilisateur connecté
#     Si l'utilisateur a été supprimé on supprimé la séance qu'il a commandée
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    seance = models.ForeignKey(Seance, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    # savoir si la séance été commandée
    ordered = models.BooleanField(default=False) 
    ordered_date = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        if self.seance.film:
            return f"{self.seance.programme} '{self.seance.film.titre}' {self.seance.date.strftime('%d/%m/%Y')} - {self.seance.horaire} ({self.quantity})"
        else:
           return f"{self.seance.programme} '{self.seance.evenement.titre}' {self.seance.date.strftime('%d/%m/%Y')} - {self.seance.horaire} ({self.quantity})"

    @property
    def subtotal(self):
        return self.seance.prix * self.quantity
    
# Panier
class Cart(models.Model):
    # Un utilisateur ne peut avoir qu'un seul panier
    user = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE)
    # Il peut y avoir plusieurs séances commandées dans le panier
    orders = models.ManyToManyField(Order, blank=True)
      
    
    def __str__(self):
        return f"{self.user.username}"
    
    @property
    def total(self):
        return sum(order.subtotal for order in self.orders.all())
    
   
    
    