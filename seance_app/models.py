from django.db import models

class Cinema(models.Model):
    nom = models.CharField(max_length=100)
    adresse = models.TextField()
    telephone = models.CharField(max_length=20)
    
    def __str__(self):
        return self.nom

class Salle(models.Model):
    # le cinéma peut possède plusieurs salles - les salles appartiennent à un cinéma
    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE) 
    numero = models.IntegerField()
    capacite = models.IntegerField()
    disponible = models.BooleanField(default=True) # Pour savoir si la salle est encore disponible ou pas
    
    def __str__(self):
        return f'salle n°{self.numero}'

class Film(models.Model):
    titre = models.CharField(max_length=150)
    duree = models.IntegerField()
    genre = models.CharField(max_length=50)
    date_sortie = models.DateField()
    realisateur = models.CharField(max_length=100)
    description = models.TextField()
    affiche = models.ImageField(upload_to='films/')
    
    def __str__(self):
        return self.titre

class Evenement(models.Model):
    titre = models.CharField(max_length=150)
    description = models.TextField()
    genre = models.CharField(max_length=50)
    affiche = models.ImageField(upload_to='evenements/')
    
    def __str__(self):
        return self.titre

class Seance(models.Model):
    # un film peut etre projeté dans plusieurs séances - Un séance projete un film    
    # une salle peut avoir plusieurs séances - Une séance se déroule dans une salle
    film = models.ForeignKey(Film, on_delete=models.CASCADE, null=True, blank=True) # peut etre vide car dans dans un seance on aura soit un film ou un evenement
    # un evenement peut etre projeté dans plusieurs séances - Un séance projete un evenement    
    # une salle peut avoir plusieurs evenements - Un evenement se déroule dans une salle
    evenement = models.ForeignKey(Evenement, on_delete=models.CASCADE, null=True, blank=True) # peut etre vide car dans dans un seance on aura soit un film ou un evenement
    place_dispo = models.IntegerField
    salle = models.ForeignKey(Salle, on_delete=models.CASCADE)
    date = models.DateField()
    heure = models.TimeField()
    prix = models.DecimalField(max_digits=6, decimal_places=2)
    
    def __str__(self):
        return f'séance du {self.date} à {self.heure}'

