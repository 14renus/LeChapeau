from django import forms

from .models import Salle, Jouer, Mot

class SalleForm(forms.ModelForm):

    class Meta:
        model = Salle
        fields = ('id',)


