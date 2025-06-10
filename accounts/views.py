from django.dispatch import receiver
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from consultations.models import Ordonnance
from consultations.forms import OrdonnanceForm

from .models import CustomUser, DossierMedical
from .forms import CustomUserCreationForm, EditAccountForm, EntreeDossierForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.db.models.signals import post_save
#import requests

@login_required
def redirect_by_role(request):
    """Redirige vers le dashboard en fonction du rôle."""
    user = request.user
    if user.role == 'medecin':
        return redirect('dashboard_medecin')
    elif user.role == 'patient':
        return redirect('dashboard_patient')
    elif user.role == 'admin':
        return redirect('admin:index')  # Django admin
    return redirect('/')  # Page d'accueil ou fallback

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect_by_role(request)
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect_by_role(request)
        else:
            return render(request, 'accounts/login.html', {
                'error': 'Nom d’utilisateur ou mot de passe incorrect.'
            })
    return render(request, 'accounts/login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def account_view(request):
    return render(request, 'accounts/account.html', {'user': request.user})

@login_required
def edit_account_view(request):
    if request.method == 'POST':
        form = EditAccountForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('account')
    else:
        form = EditAccountForm(instance=request.user)
    return render(request, 'accounts/edit_account.html', {'form': form})


@login_required
def voir_dossier(request, patient_id):
    # Vérification des droits d'accès
    if request.user.role == 'medecin':
        dossier = get_object_or_404(DossierMedical, patient__id=patient_id)
    elif request.user.role == 'patient' and request.user.id == patient_id:
        dossier = get_object_or_404(DossierMedical, patient=request.user)
    else:
        return HttpResponseForbidden("Accès interdit.")
    
    # Liste des ordonnances du patient
    ordonnances = Ordonnance.objects.filter(patient=dossier.patient).order_by('-date')

    # Gestion du formulaire d'ajout ou modification d'ordonnance
    # On gère ici l'ajout uniquement (modification dans modal via JS)
    if request.method == 'POST' and 'ajouter_ordonnance' in request.POST:
        form = OrdonnanceForm(request.POST, request.FILES)
        if form.is_valid():
            ordonnance = form.save(commit=False)
            ordonnance.patient = dossier.patient
            ordonnance.auteur = request.user
            ordonnance.save()
            return redirect('voir_dossier', patient_id=patient_id)
    else:
        form = OrdonnanceForm()

    return render(request, 'dossiers/voir_dossier.html', {
        'dossier': dossier,
        'ordonnances': ordonnances,
        'form': form,
    })

@login_required
def modifier_ordonnance(request, ordonnance_id):
    ordonnance = get_object_or_404(Ordonnance, id=ordonnance_id)

    # Vérification des droits : médecin uniquement (auteur)
    if request.user.role != 'medecin' or ordonnance.auteur != request.user:
        return HttpResponseForbidden("Accès interdit.")

    if request.method == 'POST':
        form = OrdonnanceForm(request.POST, request.FILES, instance=ordonnance)
        if form.is_valid():
            form.save()
            return redirect('voir_dossier', patient_id=ordonnance.patient.id)
    else:
        form = OrdonnanceForm(instance=ordonnance)

    # En cas d'accès direct (rare), on peut rediriger vers dossier
    return redirect('voir_dossier', patient_id=ordonnance.patient.id)

@login_required
def ajouter_entree(request, patient_id):
    # Autoriser uniquement les médecins à ajouter une entrée
    if request.user.role != 'medecin':
        return HttpResponseForbidden("Accès interdit. Réservé aux médecins.")
    
    patient = get_object_or_404(CustomUser, id=patient_id, role='patient')
    dossier = patient.dossier

    if request.method == 'POST':
        form = EntreeDossierForm(request.POST, request.FILES)
        if form.is_valid():
            entree = form.save(commit=False)
            entree.dossier = dossier
            entree.auteur = request.user  # médecin connecté
            entree.save()
            return redirect('voir_dossier', patient_id=patient.id)
    else:
        form = EntreeDossierForm()

    return render(request, 'dossiers/ajouter_entree.html', {'form': form, 'patient': patient})



"""@login_required
def change_password_view(request):
    if request.method == 'POST':
        recaptcha_response = request.POST.get('g-recaptcha-response')
        data = {
            'secret': 'VOTRE_CLE_SECRETE_RECAPTCHA',
            'response': recaptcha_response
        }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        result = r.json()

        if result['success']:
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)
                return redirect('account')
        else:
            error = "Échec du reCAPTCHA. Veuillez réessayer."
            form = PasswordChangeForm(request.user, request.POST)
            return render(request, 'accounts/change_password.html', {'form': form, 'recaptcha_error': error})
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {'form': form})"""

