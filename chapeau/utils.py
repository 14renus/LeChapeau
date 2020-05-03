from .models import Salle
from .models import Mot
from .models import Jouer
from .models import Equipe

import random

##########################
# Actions to start a game
#########################
def GetRoomById(salle_id):
    return Salle.objects.get(id=salle_id)

# return: QuerySet[Equipe]
def GetTeams(salle_id):
    return Salle.objects.get(id=salle_id).equipe_set.all()

# return: QuerySet[Jouer]
def GetPlayers(salle_id):
    salle = GetRoomById(salle_id)
    return Jouer.objects.filter(equipe__salle=salle)

def AddWordList(salle_id, word_list):
    for mot in word_list:
        Mot.objects.get_or_create(mot=mot, salle=Salle(id=salle_id))

def AddTeamIfDoesNotExist(salle_id, equipe_nom):
    if Equipe.objects.filter(nom=equipe_nom, salle=Salle(id=salle_id)).exists():
        return
    return Equipe.objects.create(nom=equipe_nom, salle=Salle(id=salle_id))

# if equipe_nom is null, create default equipe in salle and add player
def AddPlayer(salle_id, player_nom, equipe_nom=None):
    if equipe_nom is None:
        equipe = Equipe.objects.create(salle=Salle(id=salle_id))
        equipe.save()
    else:
        equipe = Equipe.objects.get(salle=Salle(id=salle_id), nom=equipe_nom)
    player = Jouer(nom=player_nom, equipe=equipe)
    player.save()
    return player

# Choose hatter and assigned ordered indices for teams and players.
# Return str : hatter name
def ChooseHatter(salle_id):
    hatter_name = None
    team_index = 0
    team_set = GetTeams(salle_id)
    for team in team_set:
        # assign team order
        team.ordered_index = team_index
        if team_index == 0:
            team.hatter = True
        team.save()
        # assign player order
        player_index=0
        player_set = team.jouer_set.all()
        for player in player_set:
            player.ordered_index = player_index
            if player_index==0:
                # assign player hatter
                player.hatter = True
                if team_index==0:
                    hatter_name = player.nom
            player.save()
            player_index+=1
        team_index+=1
    return hatter_name

#################################################
# Actions to be performed within one round of the game.
##################################################

def IsHatter(salle_id, player_id):
    return Jouer.objects.get(salle=Salle(id=salle_id), nom=player_id).hatter

# return: liste de mots
def _GetFreeWords(salle_id):
    return Mot.objects.filter(salle=Salle(id=salle_id), libre=True, tour=False)

# return: [str list]
def GetFreeWordsList(salle_id):
    libre_mots_query = _GetFreeWords(salle_id)
    if not libre_mots_query.exists():
        return None
    return [x.mot for x in libre_mots_query]

# return: None if there are no more free words
def ChooseRandomFreeWord(salle_id):
    libre_mots = _GetFreeWords(salle_id)

    if(len(libre_mots) == 0):
        return None

    choix = libre_mots[random.randint(0, len(libre_mots)-1)]

    # tour = true
    choix.tour=True
    choix.save()

    return choix.mot

def PassWord(salle_id, mot):
    mot = Mot.objects.get(salle=Salle(id=salle_id), mot=mot)
    mot.passe = True
    mot.save()

# return: list of dicts [{mot: str, passe: bool}]
def GetWordsInRound(salle_id):
    words = Mot.objects.filter(salle=Salle(id=salle_id), tour=True)
    return [{'word':word.mot, 'passed':word.passe} for word in words]

# return: [str list]
# def GetGuessersInRound(salle_id):
#     return [jouer.nom for jouer in Jouer.objects.filter(salle=Salle(id=salle_id), hatter=False)]

# param: list of dicts [{mot: str, passe: bool, player: str}]
# def FixWordsInRound(salle_id, mot_dict_list):
#     for mot_dict in mot_dict_list:
#         if 'mot' not in mot_dict_list:
#             continue
#         # update passe
#         mot_obj = Mot.objects.get(salle=Salle(id=salle_id), mot=mot_dict['mot'])
#         if mot_obj.exists() and 'passe' in mot_dict:
#             mot_obj.passe = mot_dict['passe']
#             mot_obj.save()

# param: list of dicts [{mot: str, passe: bool, player: str}]
# TODO: update
def UpdateScoreboard(salle_id, mot_dict_list):
    return
    # hatter = Jouer.objects.filter(salle=Salle(id=salle_id), hatter=True)
    # if not hatter.exists():
    #     print("Hatter does not exist for game room ", salle_id)
    # for mot_dict in mot_dict_list:
    #     if 'mot' not in mot_dict_list:
    #         continue
    #     # update Player and Hatter scores
    #     if 'passe' in mot_dict and mot_dict['passe']!=True:
    #         hatter.score += 1
    #         hatter.save()
    #         if 'player' in mot_dict:
    #             player = Jouer.objects.get(salle=Salle(id=salle_id), nom=mot_dict['player'])
    #             if player.exists():
    #                 player.score+=1
    #                 player.save()


def FlushRound(salle_id):
    mots_du_tour = Mot.objects.filter(salle=Salle(id=salle_id), tour=True)
    # set all guessed words to not free.
    mots_du_tour.filter(passe=False).update(libre=False)
    # clear all attributes for round
    mots_du_tour.update(tour=False, passe=False)


#################################################
# Actions to be performed between rounds of the game.
##################################################

# return: dict [player: str, score: int]
# TODO: update
def GetScoreboard(salle_id):
    return
    # player_set = GetOrderedPlayers(salle_id)
    # scoreboard = {}
    # for player in player_set:
    #     scoreboard[player.nom] = player.score
    # return scoreboard

# return: QuerySet
def GetOrderedPlayers(salle_id):
    return Jouer.objects.filter(salle=Salle(id=salle_id)).order_by('order_index')

# return set : Player name
def UpdateHatter(salle_id):
    team_set = GetTeams(salle_id).order_by('ordered_index')
    curr_team_set = team_set.filter(hatter=True)
    if not curr_team_set.exists():
        raise Exception("Hatter team not set. Did you call ChooseHatter?")
    curr_team=curr_team_set[0]
    player_set = curr_team.jouer_set.order_by('ordered_index')
    curr_hatter_set = player_set.filter(hatter=True)
    if not curr_hatter_set.exists():
        raise Exception("Hatter team set but not plater hatter.")
    curr_hatter=curr_hatter_set[0]

    # update player hatter in O(1)
    curr_hatter_index = curr_hatter.ordered_index
    new_hatter_index = (curr_hatter_index+1) % len(player_set)
    player_set[curr_hatter_index].hatter=False
    player_set[curr_hatter_index].save()
    player_set[new_hatter_index].hatter=True
    player_set[new_hatter_index].save()

    # update team hatter in O(1)
    curr_team_index = curr_team.ordered_index
    new_team_index = (curr_team_index+1) % len(team_set)
    team_set[curr_team_index].hatter=False
    team_set[curr_team_index].save()
    team_set[new_team_index].hatter=True
    team_set[new_team_index].save()

    curr_hatter_set = team_set[new_team_index].jouer_set.filter(hatter=True)
    if curr_hatter_set.exists():
        return curr_hatter_set[0].nom
    else:
        raise Exception("No hatter is set.")


#################################################
# Actions to be performed between games.
##################################################

# if clear_game = True, clear words and scoreboard
# if clear_game = False, set words attributes to default
# TODO: update
def FlushGame(salle_id, clear_game=False):
   return