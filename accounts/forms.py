from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, EntreeDossier

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'telephone', 'role', 'password1', 'password2')


class EditAccountForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'telephone'] 

from django import forms
from .models import EntreeDossier

class EntreeDossierForm(forms.ModelForm):
    class Meta:
        model = EntreeDossier
        fields = ['titre', 'description', 'fichier']
        widgets = {
            'titre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Titre de l'entrée"
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': "Description détaillée"
            }),
            'fichier': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
        }

