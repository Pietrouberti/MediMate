from django.db import models
import uuid


# Standard SQL database to hold patient dataset records for frontend information retrieval
class Patients(models.Model):
    id = models.UUIDField(primary_key=True, editable=False)
    first_name = models.CharField(max_length=255, blank=False, null=False)
    last_name = models.CharField(max_length=255, blank=False, null=False)
    age = models.IntegerField()
    date_of_birth = models.DateField(blank=False, null=False)
    gender = models.CharField(max_length=255)
    ethnicity = models.CharField(max_length=255)
    address = models.TextField(max_length=500, blank=False, null=False)
     

# class PatientAppointments(models.Model):
#     id = models.UUIDField(primary_key=True, editable=False)
#     patient = models.ForeignKey(Patients, on_delete=models.CASCADE, related_name='appointments')
#     appointment_date = models.DateTimeField()
#     appointment_type = models.CharField()
#     reason = models.TextField(max_length=500, blank=False, null=False)
    

# class PatientMedication(models.Model):
#     patient = models.ForeignKey(Patients, on_delete=models.CASCADE, related_name="medications")
#     medication = models.TextField(max_length=500, blank=False, null=False)
#     start_date = models.DateField(blank=False, null=False)
#     end_date = models.DateTimeField()
    
# class PatientAllergies(models.Model):
#     patient = models.ForeignKey(Patients, on_delete=models.CASCADE, related_name='allergies')
#     start_date = models.DateField(blank=False, null=False)
#     allergy = models.
    

