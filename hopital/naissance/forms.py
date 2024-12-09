from django import forms
from .models import Naissance
from django.contrib.auth.models import User

class NaissanceForm(forms.ModelForm):
    class Meta:
        model = Naissance
        fields = ['nom_enfant', 'date_naissance', 'nom_pere', 'nom_mere', 'lieu_naissance', 'statut_validation']




class UserForm(forms.ModelForm):
    ROLE_CHOICES = [
        ('admin', 'Administrateur'),
        ('user', 'Utilisateur'),
    ]
    STATUS_CHOICES = [
        ('active', 'Actif'),
        ('inactive', 'Inactif'),
    ]
    
    role = forms.ChoiceField(choices=ROLE_CHOICES)
    status = forms.ChoiceField(choices=STATUS_CHOICES)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
