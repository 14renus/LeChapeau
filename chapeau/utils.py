from .models import Salle
from .models import Mot
from .models import Jouer

import random

##########################
# Actions to start a game
#########################
def GetRoomById(salle_id):
    return Salle.objects.get(id=salle_id)

# return: QuerySet
def GetPlayers(salle_id):
    return Jouer.objects.filter(salle=Salle(id=salle_id))

def AddWordList(salle_id, word_list):
    for mot in word_list:
        Mot.objects.get_or_create(mot=mot, salle=Salle(id=salle_id))

def AddPlayer(salle_id, player_id):
    player = Jouer(nom=player_id, salle=GetRoomById(salle_id))
    player.save()

# Choose hatter and assigned ordered indices
# Currently, hatter and order chosen at random
# return chosen hatter or None
def ChooseHatter(salle_id):
    player_set = GetPlayers(salle_id)
    if not player_set.exists():
        print("No players in game.")
        return

    index = 0
    for player in player_set:
        player.order_index = index
        if index==0:
            player.hatter=True
        player.save()
        index+=1
    return player_set[0]

#################################################
# Actions to be performed within one round of the game.
##################################################

def IsHatter(player_id):
    return Jouer.objects.get(nom=player_id).hatter

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
def GetGuessersInRound(salle_id):
    return [jouer.nom for jouer in Jouer.objects.filter(salle=Salle(id=salle_id), hatter=False)]

# param: list of dicts [{mot: str, passe: bool, player: str}]
def FixWordsInRound(salle_id, mot_dict_list):
    for mot_dict in mot_dict_list:
        if 'mot' not in mot_dict_list:
            continue
        # update passe
        mot_obj = Mot.objects.get(salle=Salle(id=salle_id), mot=mot_dict['mot'])
        if mot_obj.exists() and 'passe' in mot_dict:
            mot_obj.passe = mot_dict['passe']
            mot_obj.save()

# param: list of dicts [{mot: str, passe: bool, player: str}]
def UpdateScoreboard(salle_id, mot_dict_list):
    hatter = Jouer.objects.filter(salle=Salle(id=salle_id), hatter=True)
    if not hatter.exists():
        print("Hatter does not exist for game room ", salle_id)
    for mot_dict in mot_dict_list:
        if 'mot' not in mot_dict_list:
            continue
        # update Player and Hatter scores
        if 'passe' in mot_dict and mot_dict['passe']!=True:
            hatter.score += 1
            hatter.save()
            if 'player' in mot_dict:
                player = Jouer.objects.get(salle=Salle(id=salle_id), nom=mot_dict['player'])
                if player.exists():
                    player.score+=1
                    player.save()


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
def GetScoreboard(salle_id):
    player_set = GetOrderedPlayers(salle_id)
    scoreboard = {}
    for player in player_set:
        scoreboard[player.nom] = player.score
    return scoreboard

# return: QuerySet
def GetOrderedPlayers(salle_id):
    return Jouer.objects.filter(salle=Salle(id=salle_id)).order_by('order_index')

def UpdateHatter(salle_id):
    player_set = GetOrderedPlayers(salle_id)
    if not player_set.exists():
        print("No players")

    old_hatter_set = player_set.filter(hatter=True)
    if old_hatter_set.exists() and old_hatter_set[0].order_index is not None:
      old_hatter = old_hatter_set[0]
      old_index = list(player_set).index(old_hatter)

      # Clear old hatter
      old_hatter.hatter=False
      old_hatter.save()

      # Set new hatter
      new_index = (old_index+1)%len(player_set)
      player_set[new_index].hatter=True
      player_set[new_index].save()

    else:
        print("No order/hatter. Assigning new player order and hatter.")
        ChooseHatter(salle_id)
