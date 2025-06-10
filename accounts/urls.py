from django.urls import path
from .views import account_view, ajouter_entree, edit_account_view, modifier_ordonnance, redirect_by_role, register_view, login_view, logout_view, voir_dossier

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', redirect_by_role, name='dashboard_redirect'),
    path('account/', account_view, name='account'),
    path('account/edit/', edit_account_view, name='edit_account'),
    #path('account/change-password/', change_password_view, name='change_password'),

    path('dossier/<int:patient_id>/', voir_dossier, name='voir_dossier'),
    path('dossier/<int:patient_id>/ajouter/', ajouter_entree, name='ajouter_entree'),
    path('dossier/ordonnance/<int:ordonnance_id>/modifier/', modifier_ordonnance, name='modifier_ordonnance'),

]
