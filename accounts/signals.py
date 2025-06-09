# dossiers/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import DossierMedical
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_save, sender=User)
def creer_dossier_medical(sender, instance, created, **kwargs):
    if created and instance.role == 'patient':
        DossierMedical.objects.create(patient=instance)
