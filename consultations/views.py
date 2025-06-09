import uuid
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from accounts.models import CustomUser

from .forms import RendezVousForm
from .models import RendezVous


@login_required
def teleconsultation_view(request, room_name):
    return render(request, 'consultations/jitsi_call.html', {'room_name': room_name})

@login_required
def prendre_rendezvous(request):
    if request.method == 'POST':
        form = RendezVousForm(request.POST)
        if form.is_valid():
            rdv = form.save(commit=False)
            rdv.patient = request.user
            rdv.room_name = str(uuid.uuid4())
            rdv.save()
            return redirect('dashboard_patient')
    else:
        form = RendezVousForm()
    return render(request, 'consultations/prise_rdv.html', {'form': form})



@login_required
def dashboard_patient(request):
    rdvs = RendezVous.objects.filter(patient=request.user).order_by('-date')
    return render(request, 'dashboard/patient.html', {'rdvs': rdvs})


@login_required
def dashboard_medecin(request):
    user = request.user
    consultations_donnees = RendezVous.objects.filter(médecin=user).order_by('-date')
    rdvs_pris = RendezVous.objects.filter(patient=user).order_by('-date')

    # Récupérer tous les patients avec lesquels le médecin a eu/va avoir une consultation
    patients_ids = consultations_donnees.values_list('patient__id', flat=True).distinct()
    patients = CustomUser.objects.filter(id__in=patients_ids, role='patient')

    return render(request, 'dashboard/medecin.html', {
        'consultations_donnees': consultations_donnees,
        'rdvs_pris': rdvs_pris,
        'patients': patients,
    })

# Create your views here.
