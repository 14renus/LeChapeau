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
        Jouer.objects.create(nom='Dasha', salle=courgette)
        Jouer.objects.create(nom='Diego', salle=courgette)
        # Words
        Mot.objects.create(mot='whale',  salle=pumpkin)
        Mot.objects.create(mot='pig', salle=pumpkin)
        Mot.objects.create(mot='racoon', salle=courgette)

    def _get_words(self, Mot_query_set):
        return [mot.mot for mot in Mot_query_set]

    def test_GetPlayers(self):
        results = [player.nom for player in utils.GetPlayers(salle_id='pumpkin')]
        self.assertCountEqual(results,["Dasha","Renu","May"])

    def test_AddWordList(self):
        utils.AddWordList(salle_id='pumpkin', word_list=['camel'])

        mot1 = Mot()
        mot1.mot = 'whale'
        mot2 = Mot()
        mot2.mot = 'pig'
        mot3 = Mot()
        mot3.mot = 'camel'

        results = self._get_words(Mot.objects.filter(salle=Salle(id='pumpkin')))
        self.assertCountEqual(results, ['whale', 'pig', 'camel'])
        #self.assertQuerysetEqual(Mot.objects.filter(salle=Salle(id='pumpkin')), [repr(mot1), repr(mot2), repr(mot3)], ordered=False)

    def test_GetFreeWords(self):
        results = utils.GetFreeWordsList(salle_id='pumpkin')
        self.assertCountEqual(results, ['whale', 'pig'])

    def test_ChooseRandomFreeWord(self):
        exp_list = ['whale', 'pig']
        choice = utils.ChooseRandomFreeWord('pumpkin')
        self.assertIn(choice, exp_list)

        # random choice is removed from free list
        free_words = utils.GetFreeWordsList(salle_id='pumpkin')
        exp_list.remove(choice)
        self.assertCountEqual(free_words, exp_list)

        # passe is set to false
        mot = Mot.objects.get(salle=Salle(id='pumpkin'), mot=choice)
        self.assertFalse(mot.passe)
        # tour is set to true
        self.assertTrue(mot.tour)

    def test_PassWord(self):
        Mot.objects.create(mot='camel', salle=Salle(id='courgette'), tour=True)
        utils.PassWord(salle_id='courgette',mot='camel')

        # passed is set to true
        mot = Mot.objects.get(salle=Salle(id='courgette'),mot='camel')
        self.assertTrue(mot.passe)
        # tour is set to true
        self.assertTrue(mot.tour)

    def test_GetWordsInRound(self):
        Mot.objects.create(mot='camel', salle=Salle(id='courgette'), tour=True)
        Mot.objects.create(mot='wolf', salle=Salle(id='courgette'), tour=True)
        expected = [{'word':'camel', 'passed':False},
                    {'word':'wolf', 'passed':False}]

        results = utils.GetWordsInRound(salle_id='courgette')

        self.assertCountEqual(results, expected)

    def test_GetGuessersInRound(self):
        pass

    def test_FlushRound(self):
        pass

    def test_ChooseHatter(self):
        utils.ChooseHatter(salle_id='pumpkin')

        player_set = Jouer.objects.filter(salle=Salle(id='pumpkin'))

        found_hatter=False
        for player in player_set:
            self.assertFalse(player.order_index is None, "Order index should be set.")
            if player.hatter:
                if not found_hatter:
                    found_hatter=True
                else:
                    self.fail("Failed. Hatter is not unique.")
        self.assertTrue(found_hatter)

    def test_UpdateHatter(self):
        utils.ChooseHatter(salle_id='pumpkin')
        player_set = Jouer.objects.filter(salle=Salle(id='pumpkin'))
        pass



       

