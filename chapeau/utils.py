from .models import Salle
from .models import Mot
from .models import Jouer

import random

# Handles Mots avec un salle_id!
class MotsHandler(object):
    salle_id=""

    def __init__(self, salle_id):
        self.salle_id=salle_id


    def AjouteMotListe(self, mot_liste):
        for mot in mot_liste:
            Mot.objects.get_or_create(mot=mot, salle=Salle(id=self.salle_id))

    # return: liste de mots
    def _ObtientLibreMots(self):
        return Mot.objects.filter(salle=Salle(id=self.salle_id), libre=True, tour=False)

    def ObtientLibreMotsList(self):
        libre_mots_query = self._ObtientLibreMots()
        if not libre_mots_query.exists():
            return None
        return [x.mot for x in libre_mots_query]

    # return: None si il n'y a pas plus de mots.
    def ChoisiMot(self):
        libre_mots = self._ObtientLibreMots()

        if(len(libre_mots) == 0):
            return None

        choix = libre_mots[random.randint(0, len(libre_mots)-1)]

        # tour = true
        choix.tour=True
        choix.save()

        return choix.mot

    def PasseMot(self, mot):
        mot = Mot.objects.get(salle=Salle(id=self.salle_id), mot=mot)
        mot.passe = True
        mot.save()

    # return: list of dicts [{mot: str, devine: bool}]
    def ObtientMotsDuTour(self):
        return Mot.objects.filter(salle=Salle(id=self.salle_id), tour=True).values

    def EffaceTour(self):
        mots_du_tour = Mot.objects.filter(salle=Salle(id=self.salle_id), tour=True)
        mots_du_tour.filter(passe=False).update(libre=True)
        mots_du_tour.update(tour=False, passe=False)




