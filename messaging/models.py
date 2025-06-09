from django.db import models

from accounts.models import CustomUser

# Create your models here.

class Message(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_messages')
    contenu = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    lu = models.BooleanField(default=False)

