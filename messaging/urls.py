from django.urls import path
from . import views

urlpatterns = [
    path('', views.messagerie_home, name='messagerie_home'),
    path('<int:interlocuteur_id>/', views.messagerie_home, name='messagerie_home'),
]
