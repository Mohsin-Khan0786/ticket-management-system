from django.db import models

# Create your models here.
class DoctorModel(models.Model):
    name=models.CharField(max_length=100)
    specialization=models.CharField(max_length=100)
    contact_number=models.CharField(max_length=100)
  

    def __str__(self):
       return self.name
         
class NurseModel(models.Model):
    name=models.CharField(max_length=50)
    contact_number=models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class PatientModel(models.Model):
    name=models.CharField(max_length=30)
    age=models.IntegerField()
    doctors=models.ForeignKey(DoctorModel,on_delete=models.CASCADE, related_name='patients',null=True,blank=True)
    nurse=models.ForeignKey(NurseModel,on_delete=models.CASCADE,related_name='patients')
    date_admitted=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class HospitalModel(models.Model):
    patient=models.ForeignKey(PatientModel,on_delete=models.CASCADE,related_name='hospital_patients')
    doctor=models.ManyToManyField(DoctorModel)
    nurse=models.ForeignKey(NurseModel,on_delete=models.CASCADE,related_name='hospital_nurses')
    
    def __str__(self):
        return f"Hospital Record of {self.patient.name}"


class MedicalRecord(models.Model):
    patient=models.ForeignKey(PatientModel,on_delete=models.CASCADE,related_name='medical_records')
    diagnoses=models.TextField()
    precription=models.TextField()

    def __str__(self):
        return f"medical record of {self.patient.name}"

class NotificationModel(models.Model):

    message=models.CharField(max_length=150)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"message {self.message}"