import uuid
from django.db import models

# Create your models here.

from VitaLink import settings
from accounts.models import CustomUser

def generate_room_name():
    return str(uuid.uuid4())

class RendezVous(models.Model):
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='rdv_patient')
    médecin = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='rdv_medecin')
    date = models.DateTimeField()
    room_name = models.CharField(max_length=100, unique=True, default=generate_room_name)

    def jitsi_url(self):
        return f"https://meet.jit.si/{self.room_name}"

    def __str__(self):
        return f"{self.patient.username} avec {self.médecin.username} le {self.date}"

class Ordonnance(models.Model):
    consultation = models.ForeignKey(RendezVous, on_delete=models.CASCADE)
    contenu = models.TextField()
    date = models.DateField(auto_now_add=True)
    fichier = models.FileField(upload_to='ordonnances/', blank=True, null=True)


