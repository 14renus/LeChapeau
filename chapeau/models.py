from django.conf import settings
from django.db import models
import json

class Salle(models.Model):
    id = models.CharField("Nom de la salle", max_length=256, primary_key=True, default="")
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
    mot = models.CharField("Mot", max_length=256, default="")
    salle = models.ForeignKey(Salle, on_delete=models.CASCADE)  # Salle-Mot is one-to-many.
    libre = models.BooleanField("Est-ce que le mot est libre?", default=True)

    # specifique a un tour
    # si un mot est dans un tour, le mot peut etre passé (passe=True) ou deviné (passe=False))
    passe = models.BooleanField("Est-ce que le mot est passé?", default=False)
    tour = models.BooleanField("Currently in tour", default=False)

    # unique contraint
    class Meta:
        unique_together = (('mot', 'salle'))


class Jouer(models.Model):
    nom = models.CharField("Nom de le jouer", max_length=256)
    salle = models.ForeignKey(Salle, on_delete=models.CASCADE)  # Salle-Jouer is one-to-many.
    hatter = models.BooleanField("Etat de  le jouer", default=False)
    score = models.IntegerField(default=0)

    order_index = models.IntegerField(default=None, null=True)

    # unique contraint
    class Meta:
        unique_together = (('nom', 'salle'),('order_index', 'salle'))
