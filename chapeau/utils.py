from .models import Salle
from .models import Mot
from .models import Jouer

def AjouteMotListe(salle_id, mot_liste):
    for mot in mot_liste:
        Mot.objects.get_or_create(mot=mot, salle=Salle(id=salle_id))