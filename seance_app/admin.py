from django.contrib import admin
from .models import Cinema, Salle, Film, Seance, Evenement

admin.site.register(Cinema)
admin.site.register(Salle)
admin.site.register(Film)
admin.site.register(Seance)
admin.site.register(Evenement)
