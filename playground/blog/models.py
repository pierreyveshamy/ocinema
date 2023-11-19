from django.conf import settings
from django.db import models
from django.utils import timezone
 
class Room(models.Model):
    id_room = models.CharField(max_length=100, primary_key=True)
    disponibilite = models.CharField(max_length=20, default='dispo')
    photo = models.CharField(max_length=200)
    
    def __str__(self):
        return self.id_room
 

class Film(models.Model):
    id_film = models.CharField(max_length=100, primary_key=True)
    etat = models.CharField(max_length=30, default="Non diffusé aujourd'hui")
    titre = models.CharField(max_length=30)
    auteur = models.CharField(max_length=20)
    genre = models.CharField(max_length=20)
    synopsis = models.CharField(max_length=1000, default='Pas de synopsis disponible')
    affiche = models.CharField(max_length=200)
    salle = models.ForeignKey(Room, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.id_film