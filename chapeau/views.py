from django.shortcuts import render, redirect
from .forms import SalleForm
from .models import Salle

# Create your views here.
def CreerSalle(request):
    # If the form was submitted
    if request.method == "POST":
        form = SalleForm(request.POST)
        if form.is_valid():
            salle = form.save()
            return redirect('ajoute_jouers', salle_id=salle.id)
        else:
            # Salle with this name already exists, redirect to the initial page
            return render(request, 'startup.html', {"form": form, "form_errors": form.errors})
    # If the form was not submitted yet
    form = SalleForm()
    return render(request, 'startup.html', {"form": form})

def AjouteJoeurs(request, salle_id):
    return render(request, 'ajoute_jouers.html', {})

def DevineurVue(request, salle_id, jouer_id, hatter_id):
    return render(request, 'devineur_vue.html', {})

def HatterVue(request, salle_id, jouer_id, hatter_id):
    return render(request, 'hatter_vue.html', {})
