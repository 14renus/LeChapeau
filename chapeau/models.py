from django.conf import settings
from django.db import models

class Salle(models.Model):
    id = models.CharField(max_length=30)