from django.contrib import admin

# Register your models here.
from .models import Salle, Jouer, Mot

admin.site.register(Salle)
admin.site.register(Jouer)
admin.site.register(Mot)
