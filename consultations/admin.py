from django.contrib import admin
from .models import RendezVous, Ordonnance

@admin.register(RendezVous)
class RendezVousAdmin(admin.ModelAdmin):
    list_display = ('patient', 'medecin', 'date', 'room_name')
    search_fields = ('patient__username', 'medecin__username')
    list_filter = ('date',)

@admin.register(Ordonnance)
class OrdonnanceAdmin(admin.ModelAdmin):
    list_display = ('patient', 'auteur', 'date')

