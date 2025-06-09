from django.db import models
# Create your models here.

from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('patient', 'Patient'),
        ('medecin', 'Médecin'),
        ('admin', 'Administrateur'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='patient')
    telephone = models.CharField(max_length=22, default='')


class PatientProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    date_naissance = models.DateField(null=True, blank=True)
    adresse = models.TextField(blank=True)

class DoctorProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    spécialité = models.CharField(max_length=100)
    numéro_rpps = models.CharField(max_length=20)

class DossierMedical(models.Model):
    patient = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='dossier')
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Dossier de {self.patient.get_full_name()}"

class EntreeDossier(models.Model):
    dossier = models.ForeignKey(DossierMedical, on_delete=models.CASCADE, related_name='entrees')
    date = models.DateTimeField(auto_now_add=True)
    titre = models.CharField(max_length=255)
    description = models.TextField()
    auteur = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='entrees_medicales')  # généralement médecin
    fichier = models.FileField(upload_to='documents_dossier/', blank=True, null=True)

    def __str__(self):
        return f"{self.titre} - {self.date.strftime('%d/%m/%Y')}"
