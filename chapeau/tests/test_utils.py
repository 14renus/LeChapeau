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
        Jouer.objects.create(nom='Dasha', equipe=rose, salle=pumpkin)
        Jouer.objects.create(nom='Diego', equipe=rose, salle=pumpkin)
        Jouer.objects.create(nom='Renu', equipe=violet, salle=pumpkin)
        Jouer.objects.create(nom='May', equipe=violet, salle=pumpkin)

        Jouer.objects.create(nom='Dasha', equipe=rose2, salle=courgette)
        Jouer.objects.create(nom='Etienne', equipe=violet2, salle=courgette)
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

        # mot1 = Mot()
        # mot1.mot = 'whale'
        # mot2 = Mot()
        # mot2.mot = 'pig'
        # mot3 = Mot()
        # mot3.mot = 'camel'

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
        utils.AddPlayer(salle_id='courgette', player_nom='Mom', equipe_nom='violet')

        salle = Salle.objects.get(id='courgette')
        equipe = Equipe.objects.get(nom='violet', salle=salle)
        Jouer.objects.get(nom='Mom', equipe=equipe)

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

    # def test_GetWordsInRound(self):
    #     Mot.objects.create(mot='camel', salle=Salle(id='courgette'), tour=True)
    #     Mot.objects.create(mot='wolf', salle=Salle(id='courgette'), tour=True)
    #     expected = [{'word':'camel', 'passed':False},
    #                 {'word':'wolf', 'passed':False}]
    #
    #     results = utils.GetWordsInRound(salle_id='courgette')
    #
    #     self.assertCountEqual(results, expected)

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
        chosen_hatter, game_round = utils.ChooseHatter(salle_id='pumpkin', game_round=0)

        # team_set = Equipe.objects.filter(salle=Salle(id='pumpkin'))
        #
        # found_hatter_name = None
        # found_team_hatter = False
        # for team in team_set:
        #     self.assertFalse(team.ordered_index is None, "Team order index should be set.")
        #     if team.hatter:
        #         if not found_team_hatter:
        #             found_team_hatter = True
        #         else:
        #             self.fail("Failed. Team hatter is not unique.")
        #     found_player_hatter = False
        #     player_set = team.jouer_set.all()
        #     for player in player_set:
        #         if player.hatter:
        #             if not found_player_hatter:
        #                 found_player_hatter=True
        #             else:
        #                 self.fail("Failed. Player hatter is not unique.")
        #             if team.hatter:
        #                 hatter_name=player.nom
        #     self.assertTrue(found_player_hatter, "No player hatter found.")
        # self.assertTrue(found_team_hatter, "No team hatter found.")
        # self.assertTrue(hatter_name==chosen_hatter)
        self.assertEquals(chosen_hatter, 'Dasha')
        self.assertEquals(game_round, 1)

        # If the hatter was already chosen, no changes will be applied
        new_hatter, game_round = utils.ChooseHatter(salle_id='pumpkin', game_round=0)
        self.assertEquals(new_hatter, 'Dasha')
        self.assertEquals(game_round, 1)

        # Team hatter and order is set
        rose = Equipe.objects.get(salle=Salle(id='pumpkin'), nom='rose')
        violet = Equipe.objects.get(salle=Salle(id='pumpkin'), nom='violet')
        self.assertTrue(rose.hatter)
        self.assertEqual(rose.ordered_index, 0)
        self.assertFalse(violet.hatter)
        self.assertEqual(violet.ordered_index, 1)

        # Player Hatter and order for each team is  set
        dasha = Jouer.objects.get(nom='Dasha', equipe=rose)
        diego = Jouer.objects.get(nom='Diego', equipe=rose)
        renu = Jouer.objects.get(nom='Renu', equipe=violet)
        may = Jouer.objects.get(nom='May', equipe=violet)
        self.assertTrue(dasha.hatter)
        self.assertEqual(dasha.ordered_index, 0)
        self.assertFalse(diego.hatter)
        self.assertEqual(diego.ordered_index, 1)
        self.assertTrue(renu.hatter)
        self.assertEqual(renu.ordered_index, 0)
        self.assertFalse(may.hatter)
        self.assertEqual(may.ordered_index, 1)


    def test_UpdateHatter(self):
        #### 1. set order and first hatter
        first_hatter, game_round = utils.ChooseHatter(salle_id='pumpkin', game_round=0)
        self.assertEquals(first_hatter, 'Dasha')
        self.assertEquals(game_round, 1)

        salle = Salle.objects.get(id="pumpkin")

        #### 2. Next hatter = Renu in Violet
        chosen_hatter, game_round = utils.UpdateHatter(salle)
        # Correct hatter
        self.assertEquals(chosen_hatter, 'Renu')
        self.assertEquals(game_round, 2)
        # Update team
        rose = Equipe.objects.get(salle=Salle(id='pumpkin'), nom='rose')
        violet = Equipe.objects.get(salle=Salle(id='pumpkin'), nom='violet')
        self.assertFalse(rose.hatter)
        self.assertTrue(violet.hatter)
        # Update Players in rose
        dasha = Jouer.objects.get(nom='Dasha', equipe=rose)
        diego = Jouer.objects.get(nom='Diego', equipe=rose)
        self.assertFalse(dasha.hatter)
        self.assertTrue(diego.hatter)

        #### 2. Next hatter = Diego in Rose
        chosen_hatter, game_round = utils.UpdateHatter(salle)
        # Correct hatter
        self.assertEquals(chosen_hatter, 'Diego')
        self.assertEquals(game_round, 3)
        # Update teame
        rose = Equipe.objects.get(salle=Salle(id='pumpkin'), nom='rose')
        violet = Equipe.objects.get(salle=Salle(id='pumpkin'), nom='violet')
        self.assertTrue(rose.hatter)
        self.assertFalse(violet.hatter)
        # Update Players in violet
        renu = Jouer.objects.get(nom='Renu', equipe=violet)
        may = Jouer.objects.get(nom='May', equipe=violet)
        self.assertFalse(renu.hatter)
        self.assertTrue(may.hatter)


        #### 3. Next hatter = May in Violet
        chosen_hatter, game_round = utils.UpdateHatter(salle)
        self.assertEquals(chosen_hatter, 'May')
        self.assertEquals(game_round, 4)

        #### 4. Next hatter = Dasha in Rose
        chosen_hatter, game_round = utils.UpdateHatter(salle)
        self.assertEquals(chosen_hatter, 'Dasha')
        self.assertEquals(game_round, 5)


    def test_FinishRound(self):
        pumpkin = Salle.objects.get(id='pumpkin')
        first_hatter, game_round = utils.ChooseHatter(salle_id='pumpkin', game_round=0)
        self.assertEquals(first_hatter, 'Dasha')
        self.assertEquals(game_round, 1)

        #### Finish round 1
        Mot.objects.create(mot='kangaroo', salle=pumpkin, tour=True, devine=True)
        Mot.objects.create(mot='otter', salle=pumpkin, tour=True, passe=True)
        Mot.objects.create(mot='doggy', salle=pumpkin, tour=True, devine=True)

        new_hatter, next_round = utils.UpdateScoreBoardAndHatter("pumpkin", 1)
        self.assertEquals(next_round, 2)
        self.assertEquals(new_hatter, 'Renu')
        # 2 words guessed, 1 word passed -> +1 score to rose
        self.assertEquals(Equipe.objects.get(salle=Salle(id='pumpkin'), nom='rose').score, 1)
        self.assertEquals(Equipe.objects.get(salle=Salle(id='pumpkin'), nom='violet').score, 0)
        utils.FlushRound('pumpkin')

        #### Round 1 was already finished and hatter updated, so no changes here.
        new_hatter, next_round = utils.UpdateScoreBoardAndHatter("pumpkin", 1)
        self.assertEquals(next_round, 2)
        self.assertEquals(new_hatter, 'Renu')

        #### Finish round 2
        Mot.objects.create(mot='elephant', salle=pumpkin, tour=True, devine=True)
        Mot.objects.create(mot='panda', salle=pumpkin, tour=True, devine=True)
        Mot.objects.filter(mot='otter', salle=pumpkin).update(tour=True, devine=True)

        new_hatter, next_round = utils.UpdateScoreBoardAndHatter("pumpkin", 2)
        self.assertEquals(next_round, 3)
        self.assertEquals(new_hatter, 'Diego')
        self.assertEquals(Equipe.objects.get(salle=Salle(id='pumpkin'), nom='rose').score, 1)
        # 3 words guessed
        self.assertEquals(Equipe.objects.get(salle=Salle(id='pumpkin'), nom='violet').score, 3)
        utils.FlushRound('pumpkin')





       

