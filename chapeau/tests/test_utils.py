from django.test import TestCase
from .. import utils
from ..models import Salle
from ..models import Mot
from ..models import Jouer

class RoundUtilsTest(TestCase):

    def setUp(self):
        # Rooms
        pumpkin = Salle.objects.create(id='pumpkin')
        courgette = Salle.objects.create(id='courgette')
        # Players
        Jouer.objects.create(nom='Dasha', salle=pumpkin)
        Jouer.objects.create(nom='Renu', salle=pumpkin)
        Jouer.objects.create(nom='May', salle=pumpkin)
        # Words
        Mot.objects.create(mot='whale',  salle=pumpkin)
        Mot.objects.create(mot='pig', salle=pumpkin)
        Mot.objects.create(mot='racoon', salle=courgette)

    def test_AddWordList(self):
        utils.AddWordList(salle_id='pumpkin', word_list=['camel'])

        mot1 = Mot()
        mot1.mot = 'whale'
        mot2 = Mot()
        mot2.mot = 'pig'
        mot3 = Mot()
        mot3.mot = 'camel'

        results = [mot.mot for mot in Mot.objects.filter(salle=Salle(id='pumpkin'))]
        self.assertCountEqual(results, ['whale', 'pig', 'camel'])
        #self.assertQuerysetEqual(Mot.objects.filter(salle=Salle(id='pumpkin')), [repr(mot1), repr(mot2), repr(mot3)], ordered=False)

    def test_GetFreeWords(self):
        results = utils.GetFreeWordsList(salle_id='pumpkin')
        self.assertCountEqual(results, ['whale', 'pig'])

       

