from django.shortcuts import render, redirect
from .forms import SalleForm
from .models import Salle

# Create your views here.
def create_room(request, already_exists=False):
    print ("welcome")
    # If the form was submitted
    if request.method == "POST":
        form = SalleForm(request.POST)
        if form.is_valid():
            salle_id = form.cleaned_data['id']
            print ('salle_id', salle_id)
            # Salle with this name already exists, redirect to the initial page
            if Salle.objects.filter(id = salle_id).exists():
                print ('already exists!')
                return redirect('create_room', already_exists=True)
            salle = form.save()
            return redirect('add_players', salle_id = salle.id)
    # If the form was not submitted yet
    form = SalleForm()
    return render(request, 'startup.html', {"form" : form, "salle_already_exists" : already_exists})

def add_players(request, salle_id):
    return render(request, 'add_players.html', {})


