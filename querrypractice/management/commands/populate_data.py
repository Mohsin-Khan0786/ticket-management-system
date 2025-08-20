from django.core.management.base import BaseCommand
import random 
from faker import Faker
from querrypractice.models import DoctorModel,NurseModel,PatientModel,HospitalModel,MedicalRecord

faker = Faker()
class Command(BaseCommand):

    def handle(self,*args,**kwargs):
        
        doctors=[]
        for _ in range(10):
            doctor=DoctorModel.objects.create(
                name=faker.name(),
                specialization=faker.job(),
                contact_number=faker.phone_number()
            )
            doctors.append(doctor)


        nurses=[]
        for _ in range(5):
            nurse=NurseModel.objects.create(
                name=faker.name_female(),
                contact_number=faker.phone_number()
            )
            nurses.append(nurse)  

        patients=[]
        for _ in range(15):
            patient=PatientModel.objects.create(
               name=faker.name(),
               age=random.randint(1,80),
               nurse=random.choice(nurses),
               doctors=random.choice(doctors)
            )
            assigned_doctor = random.choice(doctors)
            patient.doctors = assigned_doctor
            patient.save()


        for patient in patients:
            hospital=HospitalModel.objects.create(
            patient=patient,
            nurse=patient.nurse  
        )    
            hospital.doctor.add(random.choice(doctors))    

        for patient in patients:
            MedicalRecord.objects.create(
                patient=patient,
                diagnoses=faker.text(),
                 precription=faker.text()

            )




