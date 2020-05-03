from django.shortcuts import render, redirect
from .forms import RoomForm, PlayerForm, StartGameForm
from .utils import *

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
    if request.method == "POST":
        form = PlayerForm(request.POST)
        if form.is_valid():
            words = form.cleaned_data['words']
            player_id = form.cleaned_data['player_id']
            team_id = form.cleaned_data['team_id']
            AddWordList(room_id, words.split(','))
            # TODO: throw a readable error if a player with this name already exists in the game
            AddTeamIfDoesNotExist(room_id, team_id)
            AddPlayer(room_id, player_id, team_id)
            return redirect('start_game', room_id=room_id, player_id=player_id)
    form = PlayerForm()
    return render(request, 'add_players.html', {"form" : form})

def StartGameView(request, room_id, player_id):
    if request.method == "POST":
        form = StartGameForm(request.POST)
        if form.is_valid():
            if player_id == ChooseHatter(room_id):
                return redirect('hatter_preview', room_id=room_id, player_id=player_id)
            else:
                return redirect('guesser', room_id=room_id, player_id=player_id)
    # Assign order, choose Hatter
    return render(request, 'start_game.html', {})

def GuesserPreview(request, room_id, player_id):
    if request.method == "POST":
        if 'next_turn' in request.POST:
            return redirect('round_results', room_id=room_id, player_id=player_id)
        if 'game_over' in request.POST:
            return redirect('game_over', room_id=room_id, player_id=player_id)
    return render(request, 'guesser.html', {})

def HatterPreview(request, room_id, player_id):
    if request.method == "POST":
        if 'ready' in request.POST:
            return redirect('hatter_round', room_id=room_id, player_id=player_id)
    return render(request, 'hatter_preview.html', {})

def HatterView(request, room_id, player_id):
    if request.method == "POST":
        if 'next_word' in request.POST:
            return redirect('hatter_round', room_id=room_id, player_id=player_id)
        if 'skip_word' in request.POST:
            word = request.POST['word']
            if word != "None":
                PassWord(room_id, request.POST['word'])
            return redirect('hatter_round', room_id=room_id, player_id=player_id)
        if 'next_turn' in request.POST:
            return redirect('round_results', room_id=room_id, player_id=player_id)
        if 'game_over' in request.POST:
            return redirect('game_over', room_id=room_id, player_id=player_id)
    word = ChooseRandomFreeWord(room_id)
    error = None
    if not word:
        error = "Il n'y a plus de mots :("
    return render(request, 'hatter_round.html', {"word": word, "error": error})

def RoundResultsView(request, room_id, player_id):
    if request.method == "POST":
        if 'next_turn' in request.POST:
            FlushRound(room_id)
            UpdateHatter(room_id)
            # TODO: remove IsHatter
            if player_id == UpdateHatter(room_id):
                return redirect('hatter_round', room_id=room_id, player_id=player_id)
            else:
                return redirect('guesser', room_id=room_id, player_id=player_id)
        if 'game_over' in request.POST:
            return redirect('game_over', room_id=room_id, player_id=player_id)
    # TODO: display the words from the finished round in the template
    round_words = GetWordsInRound(room_id)
    return render(request, 'round_results.html', {"words": round_words})


def EndGameView(request, room_id, player_id):
    return render(request, 'game_over.html', {})


