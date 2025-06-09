import uuid
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

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
            rdv.patient = request.user  # ➕ patient automatiquement
            rdv.room_name = str(uuid.uuid4())  # 🔒 room Jitsi
            rdv.save()
            return redirect('dashboard_patient')
    else:
        form = RendezVousForm()
    return render(request, 'consultations/prise_rdv.html', {'form': form})


@login_required
def dashboard_patient(request):
    rdvs = RendezVous.objects.filter(patient=request.user).order_by('-date')
    return render(request, 'dashboard/patient.html', {'rdvs': rdvs})

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from consultations.models import RendezVous

@login_required
def dashboard_medecin(request):
    user = request.user
    consultations_donnees = RendezVous.objects.filter(médecin=user)
    rdvs_pris = RendezVous.objects.filter(patient=user)

    return render(request, 'dashboard/medecin.html', {
        'consultations_donnees': consultations_donnees,
        'rdvs_pris': rdvs_pris,
    })

# Create your views here.
