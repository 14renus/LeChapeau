from django.shortcuts import render, redirect
from .forms import SalleForm
from .models import Salle

# Create your views here.
def create_room(request):
    print ("welcome")
    # If the form was submitted
    if request.method == "POST":
        form = SalleForm(request.POST)
        if form.is_valid():
            salle = form.save()
            return redirect('add_players', salle_id=salle.id)
        else:
            # Salle with this name already exists, redirect to the initial page
            print ('already exists!')
            return render(request, 'startup.html', {"form" : form, "form_errors" : form.errors})
    # If the form was not submitted yet
    form = SalleForm()
    return render(request, 'startup.html', {"form" : form})

def add_players(request, salle_id):
    return render(request, 'add_players.html', {})

def guesser_view(request, salle_id, jouer_id, hatter_id):
    return render(request, 'guesser_view.html', {})

def hatter_view(request, salle_id, jouer_id, hatter_id):
    return render(request, 'guesser_view.html', {})
