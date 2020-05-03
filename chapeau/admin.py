from django.contrib import admin

# Register your models here.
from .models import Salle, Jouer, Mot, Equipe

admin.site.register(Salle)
admin.site.register(Jouer)
admin.site.register(Mot)
admin.site.register(Equipe)