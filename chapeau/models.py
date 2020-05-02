from django.conf import settings
from django.db import models

class Salle(models.Model):
    id = models.CharField("Nom de la salle", max_length=30, primary_key=True)
