# urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Route pour le dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Routes pour la gestion des utilisateurs
    path('utilisateurs/', views.gestion_utilisateurs, name='gestion_utilisateurs'),
    path('utilisateurs/ajouter/', views.ajouter_utilisateur, name='ajouter_utilisateur'),
    path('utilisateurs/modifier/<int:user_id>/', views.modifier_utilisateur, name='modifier_utilisateur'),
    path('gestion_naissances/', views.gestion_naissances, name='gestion_naissances'),
    path('modifier/<int:naissance_id>/', views.modifier_naissance, name='modifier_naissance'),


    # Routes pour la gestion des actes de naissance
    path('gestion_actes/', views.gestion_actes, name='gestion_actes'),
    path('actes/', views.liste_actes, name='liste_actes'),
    path('valider-acte/<str:id_acte>/', views.valider_acte, name='valider_acte'),
    path('acte/<int:acte_id>/', views.details_acte, name='details_acte'),
    path('acte/ajouter/', views.ajouter_acte, name='ajouter_acte'),
    path('acte/modifier/<int:acte_id>/', views.modifier_acte, name='modifier_acte'),
    path('rapport_mensuel/', views.rapport_mensuel, name='rapport_mensuel'),

]
