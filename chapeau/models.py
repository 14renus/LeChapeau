from django.conf import settings
from django.db import models
import json

class Salle(models.Model):
    id = models.CharField("Nom de la salle", max_length=256, primary_key=True, default="")

    PARTICULIER="Particulier"
    EQUIPE="Equipe"
    GAME_MODE_CHOICES = (
        (PARTICULIER, "Chaque jouer joue pour lui-meme."),
        (PARTICULIER, "Les jouers son dividé en équipes."),
    )
    mode = models.CharField("Nom de la salle", max_length=256, choices=GAME_MODE_CHOICES, default='Equipe')

class  Mot(models.Model):
    mot = models.CharField("Mot", max_length=256, default="")
    salle = models.ForeignKey(Salle, on_delete=models.CASCADE, db_index=True)  # Salle-Mot is one-to-many.
    libre = models.BooleanField("Est-ce que le mot est libre?", default=True)

    # specifique a un tour
    # si un mot est dans un tour, le mot peut etre passé (passe=True) ou deviné (passe=False))
    passe = models.BooleanField("Est-ce que le mot est passé?", default=False)
    tour = models.BooleanField("Currently in tour", default=False)

    # unique constraint
    class Meta:
        constraints = [
            models.UniqueConstraint(fields= ['mot','salle'], name='unique words in room'),
        ]

class Equipe(models.Model):
    nom = models.CharField("Nom de l'equipe", max_length=256, default="")
    salle = models.ForeignKey(Salle, on_delete=models.CASCADE, db_index=True)  # Salle-Jouer is one-to-many.
    score = models.IntegerField(default=0)
    ordered_index = models.IntegerField(default=None, null=True) # order of team within game
    hatter = models.BooleanField("Etat de  l'equipe (hatter/guesser)?", default=False)

    # unique constraint
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['nom', 'salle'], name='unique team in game room'),
            models.UniqueConstraint(fields=['ordered_index', 'salle'], name='unique team order in game room'),
        ]


class Jouer(models.Model):
    nom = models.CharField("Nom de le jouer", max_length=256, blank=False)
    #salle = models.ForeignKey(Salle, on_delete=models.CASCADE)  # Salle-Jouer is one-to-many.
    equipe = models.ForeignKey(Equipe, on_delete=models.CASCADE, db_index=True)  # Equipe-Jouer is one-to-many.
    hatter = models.BooleanField("Etat de  le jouer (hatter/guesser)", default=False)

    ordered_index = models.IntegerField(default=None, null=True) # order within team

    # unique constraints
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['ordered_index', 'equipe'], name='unique player order in team'),
            #models.UniqueConstraint(fields=['nom', 'equipe__salle'], name='unique player name in game room'),
        ]
