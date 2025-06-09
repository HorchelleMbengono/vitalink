from django import forms


from .models import RendezVous, Ordonnance
from .models import CustomUser

class RendezVousForm(forms.ModelForm):
    class Meta:
        model = RendezVous
        fields = ['médecin', 'date']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrer uniquement les utilisateurs ayant le rôle médecin 
        self.fields['médecin'].queryset = CustomUser.objects.filter(role='medecin')

class OrdonnanceForm(forms.ModelForm):
    class Meta:
        model = Ordonnance
        fields = ['consultation', 'contenu', 'fichier']
