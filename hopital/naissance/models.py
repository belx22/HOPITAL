from django.db import models

from django.contrib.auth.models import AbstractUser, Group, Permission


# Table Hopital
class Hopital(models.Model):
    nom_hopital = models.CharField(max_length=255)
    localisation = models.CharField(max_length=255)
    contact = models.CharField(max_length=50)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.nom_hopital


# Table Mairie
class Mairie(models.Model):
    nom_mairie = models.CharField(max_length=255)
    localisation = models.CharField(max_length=255)
    contact = models.CharField(max_length=50)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.nom_mairie


# Table Naissance
class Naissance(models.Model):
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('valide', 'Validé'),
        ('rejete', 'Rejeté'),
    ]

    nom_enfant = models.CharField(max_length=100)
    prenom_enfant = models.CharField(max_length=100)
    date_naissance = models.DateField()
    lieu_naissance = models.CharField(max_length=255)
    hopital = models.ForeignKey(Hopital, on_delete=models.CASCADE, related_name='naissances')
    nom_pere = models.CharField(max_length=100)
    nom_mere = models.CharField(max_length=100)
    statut_validation = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')

    def __str__(self):
        return f"{self.nom_enfant} {self.prenom_enfant}"


# Table ActeDeNaissance
class ActeDeNaissance(models.Model):
    FORMAT_CHOICES = [
        ('electronique', 'Électronique'),
        ('imprimable', 'Imprimable'),
    ]

    numero_acte = models.CharField(max_length=50, unique=True)
    naissance = models.OneToOneField(Naissance, on_delete=models.CASCADE, related_name='acte_de_naissance')
    date_emission = models.DateField(auto_now_add=True)
    format_document = models.CharField(max_length=20, choices=FORMAT_CHOICES)

    def __str__(self):
        return self.numero_acte


# Table Utilisateur (hérite d'AbstractUser)
class Utilisateur(AbstractUser):
    ROLE_CHOICES = [
        ('hopital', 'Hôpital'),
        ('mairie', 'Mairie'),
        ('admin', 'Admin'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    hopital = models.ForeignKey(Hopital, on_delete=models.SET_NULL, null=True, blank=True, related_name='utilisateurs')
    mairie = models.ForeignKey(Mairie, on_delete=models.SET_NULL, null=True, blank=True, related_name='utilisateurs')
    groups = models.ManyToManyField(Group, related_name='naissance_user_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='naissance_user_permissions_set', blank=True)

    def __str__(self):
        return self.username


# Table Journalisation
class Journalisation(models.Model):
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='journalisations')
    action = models.CharField(max_length=255)
    horodatage = models.DateTimeField(auto_now_add=True)
    description = models.TextField()

    def __str__(self):
        return f"Action by {self.utilisateur.username} on {self.horodatage}"


# Table Statistiques
class Statistiques(models.Model):
    periode = models.DateField()
    naissances_enregistrees = models.IntegerField()
    actes_delivres = models.IntegerField()
    localite = models.CharField(max_length=255)

    def __str__(self):
        return f"Statistiques for {self.periode} in {self.localite}"
