from django.shortcuts import render, redirect
from .forms import RoomForm, PlayerForm, StartGameForm
from .utils import *
from django.db import IntegrityError

def AreParamsValid(room_id, player_id):
    return Salle.objects.filter(id=room_id).exists() and Jouer.objects.filter(equipe__salle=Salle(id=room_id), nom=player_id).exists()

# Create your views here.
def CreateRoomView(request):
    # If the form was submitted
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save()
            return redirect('add_players', room_id=room.id)
        else:
            # room with this name already exists, redirect to the initial page
            return render(request, 'startup.html', {"form": form})
    # If the form was not submitted yet
    form = RoomForm()
    return render(request, 'startup.html', {"form": form})

def AddPlayerView(request, room_id):
    if not Salle.objects.filter(id=room_id).exists():
        return redirect('create_room')
    teams, hatter = GetLeaderBoardAndHatter(room_id)
    if request.method == "POST":
        form = PlayerForm(request.POST)
        if form.is_valid():
            words = form.cleaned_data['words']
            player_id = form.cleaned_data['player_id']
            team_id = form.cleaned_data['team_id']
            AddWordList(room_id, words.split(','))
            # TODO: throw a readable error if a player with this name already exists in the game
            AddTeamIfDoesNotExist(room_id, team_id)
            try:
                AddPlayer(room_id, player_id, team_id)
            except IntegrityError:
                form.add_error('player_id', 'Jouer avec nom "%s" existe déjà' % player_id)
                return render(request, 'add_players.html', {"form": form})
            return redirect('start_game', room_id=room_id, player_id=player_id)
    form = PlayerForm()
    return render(request, 'add_players.html', {"form" : form, "teams" : teams})

def StartGameView(request, room_id, player_id):
    if not AreParamsValid(room_id, player_id):
        return redirect('create_room')
    teams, hatter = GetLeaderBoardAndHatter(room_id)
    if request.method == "POST":
        form = StartGameForm(request.POST)
        if form.is_valid():
            hatter_id, game_round = ChooseHatter(room_id, 0)
            if player_id == hatter_id:
                return redirect('hatter_preview', room_id=room_id, player_id=player_id, game_round=game_round)
            else:
                return redirect('guesser', room_id=room_id, player_id=player_id, game_round=game_round)
    # Assign order, choose Hatter
    return render(request, 'start_game.html', {"teams" : teams, "hatter" : hatter})

def GuesserPreview(request, room_id, player_id, game_round):
    if not AreParamsValid(room_id, player_id):
        return redirect('create_room')
    teams, hatter = GetLeaderBoardAndHatter(room_id)
    if request.method == "POST":
        if 'next_turn' in request.POST:
            return redirect('round_results', room_id=room_id, player_id=player_id, game_round=game_round)
        if 'game_over' in request.POST:
            return redirect('game_over', room_id=room_id)
    return render(request, 'guesser.html', {"teams" : teams, "hatter" : hatter})

def HatterPreview(request, room_id, player_id, game_round):
    if not AreParamsValid(room_id, player_id):
        return redirect('create_room')
    teams, hatter = GetLeaderBoardAndHatter(room_id)
    if request.method == "POST":
        if 'ready' in request.POST:
            return redirect('hatter_round', room_id=room_id, player_id=player_id, game_round=game_round)
    return render(request, 'hatter_preview.html', {"teams" : teams, "hatter" : hatter})

def HatterView(request, room_id, player_id, game_round):
    if not AreParamsValid(room_id, player_id):
        return redirect('create_room')
    teams, hatter = GetLeaderBoardAndHatter(room_id)
    if request.method == "POST":
        if 'next_word' in request.POST:
            word = request.POST['word']
            if word != "None":
                GuessWord(room_id, request.POST['word'])
            return redirect('hatter_round', room_id=room_id, player_id=player_id, game_round=game_round)
        if 'skip_word' in request.POST:
            word = request.POST['word']
            if word != "None":
                PassWord(room_id, request.POST['word'])
            return redirect('hatter_round', room_id=room_id, player_id=player_id, game_round=game_round)
        if 'next_turn' in request.POST:
            return redirect('round_results', room_id=room_id, player_id=player_id, game_round=game_round)
        if 'game_over' in request.POST:
            return redirect('game_over', room_id=room_id)
    word = ChooseRandomFreeWord(room_id)
    error = None
    if not word:
        error = "Il n'y a plus de mots :("
    return render(request, 'hatter_round.html', {"word": word, "error": error, "teams" : teams, "hatter" : hatter})

def RoundResultsView(request, room_id, player_id, game_round):
    if not AreParamsValid(room_id, player_id):
        return redirect('create_room')
    round_words = GetWordsInRound(room_id)
    new_hatter, next_round = UpdateScoreBoardAndHatter(room_id, game_round)
    teams, hatter = GetLeaderBoardAndHatter(room_id)
    if request.method == "POST":
        if 'next_turn' in request.POST:
            FlushRound(room_id)
            if player_id == new_hatter:
                return redirect('hatter_preview', room_id=room_id, player_id=player_id, game_round=next_round)
            else:
                return redirect('guesser', room_id=room_id, player_id=player_id, game_round=next_round)
        if 'game_over' in request.POST:
            return redirect('game_over', room_id=room_id)
    return render(request, 'round_results.html', {"words": round_words, "teams" : teams, "hatter" : hatter})


def EndGameView(request, room_id):
    if not Salle.objects.filter(id=room_id).exists():
        return redirect('create_room')
    FlushGame(room_id)
    return render(request, 'game_over.html', {})


