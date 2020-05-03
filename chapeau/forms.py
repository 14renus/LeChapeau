from django import forms

from .models import Salle, Jouer, Mot

class RoomForm(forms.ModelForm):

    class Meta:
        model = Salle
        fields = ('id',)

class PlayerForm(forms.Form):
    words = forms.CharField()
    player_id = forms.CharField(max_length=256)
    team_id = forms.CharField(max_length=256)

class StartGameForm(forms.Form):
    pass