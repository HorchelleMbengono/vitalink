from django import views
from django.urls import path
from .views import dashboard_medecin, dashboard_patient, export_dossier_pdf, export_ordonnance_pdf, prendre_rendezvous, teleconsultation_view

urlpatterns = [
    path('consultation/<str:room_name>/', teleconsultation_view, name='teleconsultation'),
    path('rendezvous/', prendre_rendezvous, name='prendre_rendezvous'),
    path('dashboard/patient/', dashboard_patient, name='dashboard_patient'),
    path('dashboard/medecin/', dashboard_medecin, name='dashboard_medecin'),

    path('export/dossier/<int:patient_id>/', export_dossier_pdf, name='export_dossier_pdf'),
    path('export/ordonnance/<int:ordonnance_id>/', export_ordonnance_pdf, name='export_ordonnance_pdf'),
]
