from datetime import timedelta
from django.utils import timezone
from accounts.models import PatientProfile, DoctorProfile

def profil_incomplet_notification(request):
    if not request.user.is_authenticated:
        return {}

    user = request.user
    now = timezone.now()

    # Vérifie si l'utilisateur a plus de 24h
    if user.date_created + timedelta(hours=24) > now:
        return {}

    # Cas patient
    if user.role == 'patient' and not hasattr(user, 'patientprofile'):
        return {'show_profil_notification': True, 'profil_url': 'completer_profil_patient'}

    # Cas médecin
    if user.role == 'medecin' and not hasattr(user, 'doctorprofile'):
        return {'show_profil_notification': True, 'profil_url': 'completer_profil_medecin'}

    return {}
