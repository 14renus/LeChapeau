from django.conf import settings
from django.db import models
import json

class Salle(models.Model):
    nom = models.CharField("Nom de la salle", max_length=256)
    # mots = models.TextField("Tous les mots du jeu", default={})  # json dump dict
    # tour_mots = models.TextField("Les mots pour le tour en cours", default={})  # json dump dict
    #
    # def AddMots(self,new_mots):
    #     mots_dict = json.loads(self.mots)
    #     for mot in new_mots:
    #         mots_dict[mot] = 0
    #
    #     ## if it is empty, save it back to a '{}' string,
    #     ## if it is not empty, convert the dictionary back to a json string
    #     if not mots_dict:
    #         self.mots = '{}'
    #     else:
    #         self.data = json.dumps(mots_dict)
    #
    # def GetFreeMots(self, new_mots):
    #     mots_dict = json.loads(self.mots)
    #     for mot in new_mots:
    #         mots_dict[mot] = 0
    #
    #     ## if it is empty, save it back to a '{}' string,
    #     ## if it is not empty, convert the dictionary back to a json string
    #     if not mots_dict:
    #         self.mots = '{}'
    #     else:
    #         self.data = json.dumps(mots_dict)

class  Mot(models.Model):
    mot = models.CharField("Mot", max_length=256)
    salle = models.ForeignKey(Salle, on_delete=models.CASCADE)  # Salle-Mot is one-to-many.

    libre = models.BooleanField("Est libre?", default=True)

    passed = models.BooleanField("Est passed?", default=False)
    guessed = models.BooleanField("Est passed?", default=False)
    tour = models.BooleanField("Currently in tour", default=False)


class Jouer(models.Model):
    nom = models.CharField("Nom de le jouer", max_length=256)
    salle = models.ForeignKey(Salle, on_delete=models.CASCADE)  # Salle-Jouer is one-to-many.
    hatter = models.BooleanField("Etat de  le jouer", default=False)
    score = models.IntegerField(default=0)
