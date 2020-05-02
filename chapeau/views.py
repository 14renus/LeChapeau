from django.shortcuts import render, redirect
from .forms import RoomForm, PlayerForm
from .utils import AddWordList

# Create your views here.
def CreateRoom(request):
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

def AddPlayer(request, room_id):
    if request.method == "POST":
        form = PlayerForm(request.POST)
        if form.is_valid():
            words = form.cleaned_data['words']
            player_id = form.cleaned_data['player_id']
            AddWordList(words)
            AddPlayer(room_id, player_id)
            return redirect('start_game', room_id=room_id, player_id=player_id)







    return render(request, 'add_players.html', {})

def GuesserView(request, room_id, jouer_id, hatter_id):
    return render(request, 'guesser_view.html', {})

def HatterView(request, room_id, jouer_id, hatter_id):
    return render(request, 'hatter_view.html', {})
