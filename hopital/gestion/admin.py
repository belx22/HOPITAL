from django.contrib import admin
from .models import Patient, Consultation, Personnel, Admission, Medication, MedicationOrder, Invoice, Stock, Appointment

# ================================
# Enregistrement des modèles dans l'admin
# ================================

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'date_of_birth', 'gender', 'email')
    search_fields = ('first_name', 'last_name', 'email')

@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'consultation_date', 'diagnosis', 'prescription')
    list_filter = ('consultation_date', 'doctor')
    search_fields = ('patient__first_name', 'patient__last_name', 'doctor__username')

@admin.register(Personnel)
class PersonnelAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'department', 'salary', 'hire_date')
    list_filter = ('role', 'department')
    search_fields = ('user__first_name', 'user__last_name', 'role')

@admin.register(Admission)
class AdmissionAdmin(admin.ModelAdmin):
    list_display = ('patient', 'admission_date', 'discharge_date', 'status', 'room_number')
    list_filter = ('status', 'admission_date')
    search_fields = ('patient__first_name', 'patient__last_name')

@admin.register(Medication)
class MedicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'stock_quantity', 'price', 'expiration_date')
    list_filter = ('expiration_date',)
    search_fields = ('name',)

@admin.register(MedicationOrder)
class MedicationOrderAdmin(admin.ModelAdmin):
    list_display = ('medication', 'quantity_ordered', 'order_date', 'supplier_name')
    list_filter = ('order_date', 'supplier_name')
    search_fields = ('medication__name', 'supplier_name')

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('patient', 'consultation', 'total_amount', 'payment_status', 'issue_date')
    list_filter = ('payment_status', 'issue_date')
    search_fields = ('patient__first_name', 'patient__last_name', 'consultation__id')

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('medication', 'stock_quantity', 'last_updated')
    list_filter = ('last_updated',)
    search_fields = ('medication__name',)

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'appointment_date', 'status', 'reason')
    list_filter = ('status', 'appointment_date')
    search_fields = ('patient__first_name', 'patient__last_name', 'doctor__username')
