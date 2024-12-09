from django.db import models
from django.contrib.auth.models import User

# ================================
# 1. Modèle Patient
# ================================

class Patient(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female')])
    date_of_birth = models.DateField()
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    medical_history = models.TextField(null=True, blank=True)  # Historique médical
    allergies = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return f'{self.first_name} {self.last_name}'

# ================================
# 2. Modèle Consultation
# ================================

class Consultation(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(User, on_delete=models.CASCADE)  # Utilisateur en tant que médecin
    consultation_date = models.DateTimeField()
    diagnosis = models.TextField()
    prescription = models.TextField()
    
    def __str__(self):
        return f'Consultation {self.id} for {self.patient.first_name} {self.patient.last_name}'

# ================================
# 3. Modèle Personnel
# ================================

class Personnel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Utilisateur lié à un profil personnel
    role = models.CharField(max_length=50, choices=[('Doctor', 'Doctor'), ('Nurse', 'Nurse'), ('Technician', 'Technician'), ('Admin', 'Admin')])
    department = models.CharField(max_length=100, null=True, blank=True)  # Département médical (ex : chirurgie, cardiologie)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    hire_date = models.DateField()
    
    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} - {self.role}'

# ================================
# 4. Modèle Admission
# ================================

class Admission(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    admission_date = models.DateTimeField()
    discharge_date = models.DateTimeField(null=True, blank=True)
    room_number = models.CharField(max_length=20)
    status = models.CharField(max_length=20, choices=[('Admitted', 'Admitted'), ('Discharged', 'Discharged')])
    
    def __str__(self):
        return f'Admission of {self.patient.first_name} {self.patient.last_name}'

# ================================
# 5. Modèle Médicament
# ================================

class Medication(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    stock_quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    expiration_date = models.DateField()
    
    def __str__(self):
        return self.name

# ================================
# 6. Modèle Commande Médicaments
# ================================

class MedicationOrder(models.Model):
    medication = models.ForeignKey(Medication, on_delete=models.CASCADE)
    quantity_ordered = models.PositiveIntegerField()
    order_date = models.DateTimeField()
    supplier_name = models.CharField(max_length=100)
    
    def __str__(self):
        return f'Order for {self.medication.name}'

# ================================
# 7. Modèle Facture
# ================================

class Invoice(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=20, choices=[('Paid', 'Paid'), ('Pending', 'Pending')])
    issue_date = models.DateTimeField()
    
    def __str__(self):
        return f'Invoice #{self.id} for {self.patient.first_name} {self.patient.last_name}'

# ================================
# 8. Modèle Stock
# ================================

class Stock(models.Model):
    medication = models.ForeignKey(Medication, on_delete=models.CASCADE)
    stock_quantity = models.PositiveIntegerField()
    last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'Stock for {self.medication.name}'

# ================================
# 9. Modèle Rendez-vous
# ================================

class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(User, on_delete=models.CASCADE)  # Utilisateur en tant que médecin
    appointment_date = models.DateTimeField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=[('Scheduled', 'Scheduled'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')])
    
    def __str__(self):
        return f'Appointment {self.id} for {self.patient.first_name} {self.patient.last_name}'

