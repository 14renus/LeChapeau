from django.test import TestCase
from .. import utils
from ..models import Salle
from ..models import Mot
from ..models import Jouer
from ..models import Equipe

class RoundUtilsTest(TestCase):

    def setUp(self):
        # Rooms
        pumpkin = Salle.objects.create(id='pumpkin')
        courgette = Salle.objects.create(id='courgette')
        # Equipe
        rose = Equipe.objects.create(nom='rose', salle=pumpkin)
        violet = Equipe.objects.create(nom='violet', salle=pumpkin)
        rose2 = Equipe.objects.create(nom='rose', salle=courgette)
        violet2 = Equipe.objects.create(nom='violet', salle=courgette)
        # Players
        Jouer.objects.create(nom='Dasha', equipe=rose)
        Jouer.objects.create(nom='Renu', equipe=violet)
        Jouer.objects.create(nom='May', equipe=violet)
        Jouer.objects.create(nom='Diego', equipe=rose)
        Jouer.objects.create(nom='Dasha',equipe=rose2)
        Jouer.objects.create(nom='Etienne', equipe=violet2)
        # Words
        Mot.objects.create(mot='whale',  salle=pumpkin)
        Mot.objects.create(mot='pig', salle=pumpkin)
        Mot.objects.create(mot='racoon', salle=courgette)

    def _get_words(self, Mot_query_set):
        return [mot.mot for mot in Mot_query_set]

    def test_GetTeams(self):
        results = [team.nom for team in utils.GetTeams(salle_id='pumpkin')]
        self.assertCountEqual(results, ["rose", "violet"])

    def test_GetPlayers(self):
        results = [player.nom for player in utils.GetPlayers(salle_id='pumpkin')]
        self.assertCountEqual(results, ["Dasha","Renu","May","Diego"])

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

    def test_addTeamIfDoesNotExist(self):
        utils.AddTeamIfDoesNotExist(salle_id='pumpkin', equipe_nom='daisy')
        # no error should be raised.
        Equipe.objects.get(nom='daisy', salle=Salle(id='pumpkin'))
        utils.AddTeamIfDoesNotExist(salle_id='pumpkin', equipe_nom='daisy')
        # no error should be raised.
        Equipe.objects.get(nom='daisy', salle=Salle(id='pumpkin'))

    def test_AddPlayer(self):
        # Test equipe_nom=None
        utils.AddPlayer(salle_id='courgette', player_nom='Dad')

        salle = Salle.objects.get(id='courgette')
        equipe = Equipe.objects.get(nom='', salle=salle)
        Jouer.objects.get(nom='Dad', equipe=equipe)

        # Test equipe_nom!=None
        utils.AddPlayer(salle_id='courgette', player_nom='Dad', equipe_nom='violet')

        salle = Salle.objects.get(id='courgette')
        equipe = Equipe.objects.get(nom='violet', salle=salle)
        Jouer.objects.get(nom='Dad', equipe=equipe)

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

    def test_FixWordsInRound(self):
        pass

    def test_UpdateScoreboard(self):
        pass

    def test_FlushRound(self):
        pass

    # # TODO: check order is set correctly
    # Checks hatter is unique per team
    # Checks ordered_index in teams and players are not None
    def test_ChooseHatter(self):
        utils.ChooseHatter(salle_id='pumpkin')

        team_set = Equipe.objects.filter(salle=Salle(id='pumpkin'))

        found_team_hatter = False
        for team in team_set:
            self.assertFalse(team.ordered_index is None, "Team order index should be set.")
            if team.hatter:
                if not found_team_hatter:
                    found_team_hatter = True
                else:
                    self.fail("Failed. Team hatter is not unique.")
            found_player_hatter = False
            player_set = team.jouer_set.all()
            for player in player_set:
                if player.hatter:
                    if not found_player_hatter:
                        found_player_hatter=True
                    else:
                        self.fail("Failed. Player hatter is not unique.")
            self.assertTrue(found_player_hatter, "No player hatter found.")
        self.assertTrue(found_team_hatter, "No team hatter found.")

    # def test_UpdateHatter(self):
    #     player_set = Jouer.objects.filter(salle=Salle(id='pumpkin'))
    #
    #     # set dummy order index and hatter
    #     index=0
    #     for player in player_set:
    #         player.order_index = index
    #         if index==1:
    #             player.hatter=True
    #         index+=1
    #         player.save()
    #
    #     utils.UpdateHatter(salle_id='pumpkin')
    #
    #     ordered_player_set = Jouer.objects.filter(salle=Salle(id='pumpkin')).order_by("order_index")
    #     self.assertFalse(ordered_player_set[0].hatter)
    #     self.assertFalse(ordered_player_set[1].hatter)
    #     self.assertTrue(ordered_player_set[2].hatter)
    #
    #     utils.UpdateHatter(salle_id='pumpkin')
    #     self.assertTrue(ordered_player_set[0].hatter)
    #     self.assertFalse(ordered_player_set[1].hatter)
    #     self.assertFalse(ordered_player_set[2].hatter)






       

