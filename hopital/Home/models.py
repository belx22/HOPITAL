from django.db import models
from django.contrib.auth.models import AbstractUser

# Modèle pour les utilisateurs
class User(AbstractUser):
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Doctor', 'Doctor'),
        ('User', 'User'),
    ]
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='User')

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',  # Remplace le nom par défaut
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions_set',  # Remplace le nom par défaut
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )
# Modèle pour les docteurs
class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialty = models.CharField(max_length=255)
    biography = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='doctors/', blank=True, null=True)

# Modèle pour les services
class Service(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

# Modèle pour les horaires d'ouverture
class OpeningHour(models.Model):
    DAY_CHOICES = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]
    day_of_week = models.CharField(max_length=10, choices=DAY_CHOICES)
    opening_time = models.TimeField()
    closing_time = models.TimeField()

# Modèle pour les rendez-vous
class Appointment(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')

# Modèle pour les blogs
class Blog(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    published_date = models.DateTimeField(auto_now_add=True)

# Modèle pour les statistiques
class Statistic(models.Model):
    metric_name = models.CharField(max_length=255)
    metric_value = models.PositiveIntegerField(default=0)

# Modèle pour les newsletters
class Newsletter(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

# Modèle pour les FAQ
class FAQ(models.Model):
    question = models.TextField()
    answer = models.TextField()

# Modèle pour les témoignages
class Testimonial(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    content = models.TextField()
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
