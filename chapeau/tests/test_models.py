from django.test import TestCase
from django.db.utils import IntegrityError
from ..models import Salle
from ..models import Equipe
from ..models import Mot
from ..models import Jouer

class ModelTest(TestCase):
    def setUp(self):
        # Rooms
        pomme = Salle.objects.create(id='pomme')
        mangue = Salle.objects.create(id='mangue')
        # Equipe
        rose = Equipe.objects.create(nom='rose', salle=pomme)
        violet = Equipe.objects.create(nom='violet', salle=pomme)
        # Players
        # Jouer.objects.create(nom='Dasha', equipe=rose)
        # Jouer.objects.create(nom='Renu', equipe=violet)
        # Jouer.objects.create(nom='May', equipe=rose)
        # Jouer.objects.create(nom='Diego', equipe=violet)

    def test_unique_team_to_room(self):
        with self.assertRaises(IntegrityError):
            Equipe.objects.create(nom='rose', salle=Salle(id='pomme'))

    def test_unique_player_to_room(self):
        pass

