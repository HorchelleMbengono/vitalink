from django.shortcuts import render, redirect, get_object_or_404
from .models import Message
from accounts.models import CustomUser
from django.contrib.auth.decorators import login_required
from django.db.models import Q

@login_required
def messagerie_home(request, interlocuteur_id=None):
    user = request.user
    role = user.role  # suppose que tu as un champ 'role' dans CustomUser avec 'patient' ou 'medecin'

    # Récupérer les interlocuteurs selon le rôle
    if role == 'patient':
        interlocuteurs_qs = CustomUser.objects.filter(role='medecin')
    elif role == 'medecin':
        interlocuteurs_qs = CustomUser.objects.filter(role='patient')
    else:
        interlocuteurs_qs = CustomUser.objects.none()

    # Ne garder que ceux avec qui une conversation existe ou a existé
    interlocuteurs = interlocuteurs_qs.filter(
        Q(sent_messages__receiver=user) | Q(received_messages__sender=user)
    ).distinct()

    selected_interlocuteur = None
    conversation = []

    # Envoi de message
    if request.method == "POST" and interlocuteur_id:
        contenu = request.POST.get("contenu")
        if contenu:
            selected_interlocuteur = get_object_or_404(CustomUser, id=interlocuteur_id)
            Message.objects.create(sender=user, receiver=selected_interlocuteur, contenu=contenu)
            return redirect('messagerie_home', interlocuteur_id=interlocuteur_id)

    # Affichage des messages
    if interlocuteur_id:
        selected_interlocuteur = get_object_or_404(CustomUser, id=interlocuteur_id)
        conversation = Message.objects.filter(
            Q(sender=user, receiver=selected_interlocuteur) |
            Q(sender=selected_interlocuteur, receiver=user)
        ).order_by('timestamp')

        # Marquer les messages reçus comme lus
        conversation.filter(receiver=user, lu=False).update(lu=True)

    # Derniers messages et statut lu
    dernier_message_contenu = {}
    dernier_message_lu = {}
    for inter in interlocuteurs:
        last = Message.objects.filter(
            Q(sender=user, receiver=inter) | Q(sender=inter, receiver=user)
        ).order_by('-timestamp').first()
        if last:
            dernier_message_contenu[inter.id] = last.contenu
            if last.sender != user:
                dernier_message_lu[inter.id] = last.lu
            else:
                dernier_message_lu[inter.id] = True

    return render(request, "messaging/messagerie_home.html", {
        "interlocuteurs": interlocuteurs,
        "selected_interlocuteur": selected_interlocuteur,
        "conversation": conversation,
        "dernier_message_contenu": dernier_message_contenu,
        "dernier_message_lu": dernier_message_lu,
    })
