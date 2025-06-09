from django.db import models

# Create your models here.

from accounts.models import CustomUser

class RendezVous(models.Model):
    patient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='rdv_patient')
    médecin = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='rdv_médecin')
    date = models.DateTimeField()
    lien_visio = models.URLField(blank=True)

class Ordonnance(models.Model):
    consultation = models.ForeignKey(RendezVous, on_delete=models.CASCADE)
    contenu = models.TextField()
    date = models.DateField(auto_now_add=True)
    fichier = models.FileField(upload_to='ordonnances/', blank=True, null=True)

