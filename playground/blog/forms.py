from django import forms
from .models import Film

class MoveForm(forms.ModelForm):

    class Meta:
        model = Film
        fields = ('salle',)
