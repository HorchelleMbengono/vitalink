from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, EditAccountForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
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
            return redirect_by_role(user)
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
