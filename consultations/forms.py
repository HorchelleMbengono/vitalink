from django import forms
from .models import RendezVous, Ordonnance

class RendezVousForm(forms.ModelForm):
    class Meta:
        model = RendezVous
        fields = ['médecin', 'date']  # Ne pas inclure 'patient

class OrdonnanceForm(forms.ModelForm):
    class Meta:
        model = Ordonnance
        fields = ['consultation', 'contenu', 'fichier']
