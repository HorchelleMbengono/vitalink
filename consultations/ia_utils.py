from datetime import timedelta
from collections import Counter
from .models import RendezVous

def extraire_preferences_patient(rendezvous_passés):
    heures = [rdv.date.time().hour for rdv in rendezvous_passés]
    jours = [rdv.date.weekday() for rdv in rendezvous_passés]

    heures_frequentes = Counter(heures).most_common(3)
    jours_frequents = Counter(jours).most_common(2)

    return {
        "heures_pref": [h for h, _ in heures_frequentes],
        "jours_pref": [j for j, _ in jours_frequents],
    }

def generer_creneaux_potentiels(jours=7, heures_dispo=range(9, 18)):
    from datetime import datetime
    now = datetime.now()
    creneaux = []

    for i in range(1, jours + 1):
        jour = now + timedelta(days=i)
        if jour.weekday() < 5:
            for h in heures_dispo:
                dt = jour.replace(hour=h, minute=0, second=0, microsecond=0)
                creneaux.append(dt)
    return creneaux

def classer_creneaux_disponibles(patient, medecin, historique, heures_dispo=range(9, 18)):
    from django.utils.timezone import make_aware
    preferences = extraire_preferences_patient(historique)
    creneaux = generer_creneaux_potentiels(heures_dispo=heures_dispo)
    scores = []

    for creneau in creneaux:
        creneau_aware = make_aware(creneau)
        conflits = RendezVous.objects.filter(
            medecin=medecin,
            date__range=(creneau_aware - timedelta(minutes=30), creneau_aware + timedelta(minutes=30))
        )
        if conflits.exists():
            continue

        score = 0
        if creneau.hour in preferences["heures_pref"]:
            score += 2
        if creneau.weekday() in preferences["jours_pref"]:
            score += 1

        scores.append((creneau, score))

    return [dt for dt, s in sorted(scores, key=lambda x: x[1], reverse=True)[:5]]
