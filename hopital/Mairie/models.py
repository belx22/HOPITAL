from django.db import models
from django.contrib.auth.models import AbstractUser

# Modèle Utilisateur étendu pour rôles mairie
class Utilisateur(AbstractUser):
    ROLE_CHOICES = [
        ('ADMIN', 'Administrateur'),
        ('MAIRIE', 'Mairie'),
        ('HOPITAL', 'Hôpital'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    mairie = models.ForeignKey('Mairie', on_delete=models.SET_NULL, null=True, blank=True, related_name='users')

    def __str__(self):
        return f"{self.username} ({self.role})"

# Modèle pour les mairies
class Mairie(models.Model):
    nom = models.CharField(max_length=255)
    adresse = models.TextField()
    telephone = models.CharField(max_length=15)
    email = models.EmailField()

    def __str__(self):
        return self.nom

# Gestion des personnels de la mairie
class PersonnelMairie(models.Model):
    mairie = models.ForeignKey(Mairie, on_delete=models.CASCADE, related_name='personnels')
    nom = models.CharField(max_length=255)
    poste = models.CharField(max_length=100)
    telephone = models.CharField(max_length=15)
    email = models.EmailField()

    def __str__(self):
        return f"{self.nom} - {self.poste} ({self.mairie.nom})"

# Gestion des documents officiels
class DocumentOfficiel(models.Model):
    TYPE_DOCUMENT = [
        ('NAISSANCE', 'Acte de naissance'),
        ('MARIAGE', 'Certificat de mariage'),
        ('DECES', 'Certificat de décès'),
    ]
    numero = models.CharField(max_length=50, unique=True)
    type_document = models.CharField(max_length=20, choices=TYPE_DOCUMENT)
    mairie = models.ForeignKey(Mairie, on_delete=models.CASCADE, related_name='documents')
    date_emission = models.DateField()
    nom_demandeur = models.CharField(max_length=255)
    statut = models.CharField(max_length=50, default='EN_ATTENTE')

    def __str__(self):
        return f"{self.type_document} #{self.numero} ({self.nom_demandeur})"

# Gestion des budgets de la mairie
class BudgetMairie(models.Model):
    mairie = models.ForeignKey(Mairie, on_delete=models.CASCADE, related_name='budgets')
    annee = models.IntegerField()
    montant_alloue = models.DecimalField(max_digits=12, decimal_places=2)
    montant_depense = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Budget {self.annee} ({self.mairie.nom})"

# Gestion des projets municipaux
class ProjetMunicipal(models.Model):
    mairie = models.ForeignKey(Mairie, on_delete=models.CASCADE, related_name='projets')
    nom = models.CharField(max_length=255)
    description = models.TextField()
    budget = models.DecimalField(max_digits=12, decimal_places=2)
    date_debut = models.DateField()
    date_fin = models.DateField(null=True, blank=True)
    statut = models.CharField(max_length=50, default='En cours')

    def __str__(self):
        return f"{self.nom} ({self.mairie.nom})"

# Suivi des résidents
class Resident(models.Model):
    mairie = models.ForeignKey(Mairie, on_delete=models.CASCADE, related_name='residents')
    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255)
    date_naissance = models.DateField()
    adresse = models.TextField()
    telephone = models.CharField(max_length=15)
    email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return f"{self.nom} {self.prenom} ({self.mairie.nom})"
