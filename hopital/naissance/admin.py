from django.contrib import admin
from .models import Hopital, Mairie, Naissance, ActeDeNaissance, Utilisateur, Journalisation, Statistiques

admin.site.register(Hopital)
admin.site.register(Mairie)
admin.site.register(Naissance)
admin.site.register(ActeDeNaissance)
admin.site.register(Utilisateur)
admin.site.register(Journalisation)
admin.site.register(Statistiques)
