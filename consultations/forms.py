from django import forms


from .models import RendezVous, Ordonnance
from .models import CustomUser
from datetime import timedelta
from django.utils import timezone

class RendezVousForm(forms.ModelForm):
    class Meta:
        model = RendezVous
        fields = ['medecin', 'date']
        widgets = {
            'date': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                    'class': 'form-control'
                },
                format='%Y-%m-%dT%H:%M'
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['medecin'].queryset = CustomUser.objects.filter(role='medecin')
        if self.instance and self.instance.date:
            self.initial['date'] = self.instance.date.strftime('%Y-%m-%dT%H:%M')

    def clean_date(self):
        date = self.cleaned_data.get('date')
        if date < timezone.now():
            raise forms.ValidationError("La date du rendez-vous doit être dans le futur.")
        return date

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        medecin = cleaned_data.get('medecin')

        if date and medecin:
            # Fenêtre de 30 minutes autour du rendez-vous
            debut = date - timedelta(minutes=30)
            fin = date + timedelta(minutes=30)

            conflits = RendezVous.objects.filter(
                medecin=medecin,
                date__range=(debut, fin)
            )

            if self.instance.pk:
                conflits = conflits.exclude(pk=self.instance.pk)

            if conflits.exists():
                raise forms.ValidationError(
                    "Ce médecin a déjà un rendez-vous prévu dans les 30 minutes autour de cette date."
                )


class OrdonnanceForm(forms.ModelForm):
    class Meta:
        model = Ordonnance
        fields = ['contenu', 'fichier']
        widgets = {
            'contenu': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Détails de l’ordonnance...'}),
            'fichier': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

