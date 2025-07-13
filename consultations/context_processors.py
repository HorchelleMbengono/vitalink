from consultations.models import Notification
from messaging.models import Message
from django.db.models import Q
from accounts.models import CustomUser

def notifications_et_conversations(request):
    if request.user.is_authenticated:
        # ✅ Récupérer les 5 dernières notifications
        notifications = Notification.objects.filter(destinataire=request.user).order_by('-date')[:5]

        # ✅ Compter les notifications non lues
        nb_notifications_non_lues = Notification.objects.filter(
            destinataire=request.user,
            lu=False
        ).count()

        # ✅ Récupérer tous les messages impliquant l'utilisateur
        messages_qs = Message.objects.filter(Q(sender=request.user) | Q(receiver=request.user))

        # ✅ Récupérer les ID uniques des interlocuteurs
        sender_ids = messages_qs.values_list('sender', flat=True)
        receiver_ids = messages_qs.values_list('receiver', flat=True)

        interlocuteurs_ids = set(sender_ids.union(receiver_ids))
        interlocuteurs_ids.discard(request.user.id)  # On enlève soi-même

        interlocuteurs = CustomUser.objects.filter(id__in=interlocuteurs_ids)

        # ✅ Nombre total de messages non lus
        nb_messages_non_lus = Message.objects.filter(receiver=request.user, lu=False).count()

    else:
        notifications = []
        nb_notifications_non_lues = 0
        interlocuteurs = []
        nb_messages_non_lus = 0

    return {
        'notifications': notifications,
        'nb_notifications_non_lues': nb_notifications_non_lues,
        'interlocuteurs': interlocuteurs,
        'nb_messages_non_lus': nb_messages_non_lus,
    }
