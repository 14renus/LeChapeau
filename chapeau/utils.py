from .models import Salle
from .models import Mot
from .models import Jouer

import random

##########################
# Actions to start a game
#########################
def GetRoomById(salle_id):
    return Salle.objects.get(id=salle_id)

def AddWordList(salle_id, word_list):
    for mot in word_list:
        Mot.objects.get_or_create(mot=mot, salle=Salle(id=salle_id))



#################################################
# Actions to be performed in one round of the game.
##################################################

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
    return Mot.objects.filter(salle=Salle(id=salle_id), tour=True).values

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


def ClearRound(salle_id):
    mots_du_tour = Mot.objects.filter(salle=Salle(id=salle_id), tour=True)
    mots_du_tour.filter(passe=False).update(libre=True)
    mots_du_tour.update(tour=False, passe=False)




