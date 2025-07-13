from django import views
from django.urls import path
from .views import annuler_rendezvous, dashboard_medecin, dashboard_patient, export_dossier_pdf, export_ordonnance_pdf, modifier_rendezvous, notifications_view, prendre_rendezvous, teleconsultation_view, verifier_ouverture_salle

urlpatterns = [
    path('consultation/<str:room_name>/', teleconsultation_view, name='teleconsultation'),
    path('verifier-salle/<str:room_name>/', verifier_ouverture_salle, name='verifier_ouverture_salle'),

    path('rendezvous/', prendre_rendezvous, name='prendre_rendezvous'),
    path('dashboard/patient/', dashboard_patient, name='dashboard_patient'),
    path('dashboard/medecin/', dashboard_medecin, name='dashboard_medecin'),

    path('export/dossier/<int:patient_id>/', export_dossier_pdf, name='export_dossier_pdf'),
    path('export/ordonnance/<int:ordonnance_id>/', export_ordonnance_pdf, name='export_ordonnance_pdf'),

    path('rendezvous/modifier/<int:pk>/', modifier_rendezvous, name='modifier_rendezvous'),
    path('rendezvous/annuler/<int:pk>/', annuler_rendezvous, name='annuler_rendezvous'),

    path('notifications/', notifications_view, name='notifications'),

]
