import uuid
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from accounts.models import CustomUser, DossierMedical

from weasyprint import HTML
from django.template.loader import render_to_string

from messaging.models import Message
from .forms import RendezVousForm
from .models import Notification, Ordonnance, RendezVous


@login_required
def teleconsultation_view(request, room_name):
    try:
        rdv = RendezVous.objects.get(room_name=room_name)
    except RendezVous.DoesNotExist:
        return HttpResponse("Salle introuvable.", status=404)

    user = request.user

    # Médecin : accès direct, ouverture automatique de la salle
    if user == rdv.médecin:
        rdv.salle_ouverte = True
        rdv.save()
        return render(request, 'consultations/jitsi_call.html', {
            'room_name': room_name,
            'username': user.get_full_name(),
            'role': 'medecin',
        })

    # Patient : attend que la salle soit ouverte par le médecin
    elif user == rdv.patient:
        if rdv.salle_ouverte:
            return render(request, 'consultations/jitsi_call.html', {
                'room_name': room_name,
                'username': user.get_full_name(),
                'role': 'patient',
            })
        else:
            return render(request, 'consultations/attente_medecin.html', {
                'room_name': room_name  # indispensable pour le polling AJAX
            })

    # Autres utilisateurs : accès interdit
    return HttpResponseForbidden("Accès non autorisé.")


from django.http import JsonResponse

@login_required
def verifier_ouverture_salle(request, room_name):
    try:
        rdv = RendezVous.objects.get(room_name=room_name)
    except RendezVous.DoesNotExist:
        return JsonResponse({'erreur': 'Salle introuvable'}, status=404)

    if request.user != rdv.patient:
        return JsonResponse({'erreur': 'Non autorisé'}, status=403)

    return JsonResponse({'salle_ouverte': rdv.salle_ouverte})


@login_required
def prendre_rendezvous(request):
    if request.method == 'POST':
        form = RendezVousForm(request.POST)
        if form.is_valid():
            rdv = form.save(commit=False)
            rdv.patient = request.user
            rdv.room_name = str(uuid.uuid4())
            rdv.save()
            Notification.objects.create(
                destinataire=rdv.medecin,
                message=f"{request.user.get_full_name()} a pris un rendez-vous pour le {rdv.date.strftime('%d/%m/%Y à %H:%M')}."
            )
            Message.objects.create(
                sender=request.user,
                receiver=rdv.medecin,
                contenu="Conversation initiée automatiquement suite à la prise de rendez-vous."
            )

            return redirect('dashboard_patient')
    else:
        form = RendezVousForm()
    return render(request, 'consultations/prise_rdv.html', {'form': form})


from django.shortcuts import get_object_or_404

@login_required
def modifier_rendezvous(request, pk):
    rdv = get_object_or_404(RendezVous, pk=pk, patient=request.user)
    if request.method == 'POST':
        form = RendezVousForm(request.POST, instance=rdv)
        if form.is_valid():
            form.save()
            Notification.objects.create(
                destinataire=rdv.medecin,
                message=f"{request.user.get_full_name()} a modifié son rendez-vous au {rdv.date.strftime('%d/%m/%Y à %H:%M')}."
            )

            return redirect('dashboard_patient')
    else:
        form = RendezVousForm(instance=rdv)
    return render(request, 'consultations/modifier_rdv.html', {'form': form})

@login_required
def annuler_rendezvous(request, pk):
    rdv = get_object_or_404(RendezVous, pk=pk, patient=request.user)
    if request.method == 'POST':
        rdv.delete()
        Notification.objects.create(
            destinataire=rdv.medecin,
            message=f"{request.user.get_full_name()} a annulé son rendez-vous prévu le {rdv.date.strftime('%d/%m/%Y à %H:%M')}."
        )

        return redirect('dashboard_patient')
    return render(request, 'consultations/annuler_rdv.html', {'rdv': rdv})



@login_required
def dashboard_patient(request):
    rdvs = RendezVous.objects.filter(patient=request.user).order_by('-date')
    return render(request, 'dashboard/patient.html', {'rdvs': rdvs})


@login_required
def dashboard_medecin(request):
    user = request.user
    consultations_donnees = RendezVous.objects.filter(medecin=user).order_by('-date')
    rdvs_pris = RendezVous.objects.filter(patient=user).order_by('-date')

    # Récupérer tous les patients avec lesquels le médecin a eu/va avoir une consultation
    patients_ids = consultations_donnees.values_list('patient__id', flat=True).distinct()
    patients = CustomUser.objects.filter(id__in=patients_ids, role='patient')

    return render(request, 'dashboard/medecin.html', {
        'consultations_donnees': consultations_donnees,
        'rdvs_pris': rdvs_pris,
        'patients': patients,
    })

def export_dossier_pdf(request, patient_id):
    dossier = DossierMedical.objects.get(patient__id=patient_id)
    entrees = dossier.entrees.all()  # depuis related_name='entrees'
    ordonnances = Ordonnance.objects.filter(patient=dossier.patient)

    html_string = render_to_string('pdf/dossier_medical.html', {
        'dossier': dossier,
        'entrees': entrees,
        'ordonnances': ordonnances,
    })

    pdf = HTML(string=html_string).write_pdf()

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="Dossier_{dossier.patient.get_full_name()}.pdf"'
    return response


def export_ordonnance_pdf(request, ordonnance_id):
    ordonnance = Ordonnance.objects.get(id=ordonnance_id)
    html_string = render_to_string('pdf/ordonnance.html', {'ordonnance': ordonnance})
    pdf = HTML(string=html_string).write_pdf()

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="Ordonnance_{ordonnance.id}.pdf"'
    return response


from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Notification

@login_required
def notifications_view(request):
    notifications = Notification.objects.filter(destinataire=request.user).order_by('-date')

    # Marquer comme lues toutes les notifications affichées
    notifications.filter(lu=False).update(lu=True)

    # Compter les non lues pour la navbar si besoin
    nb_notifications_non_lues = Notification.objects.filter(destinataire=request.user, lu=False).count()

    return render(request, 'consultations/notifications.html', {
        'notifications': notifications,
        'nb_notifications_non_lues': nb_notifications_non_lues
    })
