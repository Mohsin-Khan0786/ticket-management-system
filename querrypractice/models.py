from django.db import models

# Create your models here.
class DoctorModel(models.Model):
    name=models.CharField(max_length=30)
    specialization=models.CharField(max_length=40)
    contact_number=models.CharField(max_length=20)

    def __str__(self):
       return self.name
         
class NurseModel(models.Model):
    name=models.CharField(max_length=20)
    contact_number=models.CharField(max_length=25)

    def __str__(self):
        return self.name
    
class PatientModel(models.Model):
    name=models.CharField(max_length=30)
    age=models.IntegerField()
    doctors=models.ManyToManyField(DoctorModel,related_name='doctors')
    nurse=models.ForeignKey(NurseModel,on_delete=models.CASCADE,related_name='nurses')
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
    patient=models.ForeignKey(PatientModel,on_delete=models.CASCADE,related_name='patients')
    diagnoses=models.TextField()
    precription=models.TextField()

    def __str__(self):
        return f"medical record of {self.patient.name}"

