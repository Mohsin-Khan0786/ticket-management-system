from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count, Avg
from querrypractice.models import *
from django.db.models.functions import ExtractMonth
from django.db.models import Max, Min


class Command(BaseCommand):
    def handle(self,*args,**kwrgs):

       # 1 Retrieve all patients admitted on a specific date.
        specific_date = timezone.now().date()
        patients = PatientModel.objects.filter(date_admitted__date=specific_date)
        print([p.name for p in patients])

        # 2 Get the names of all doctors who have patients with a specific diagnosis.
        specific_diagnosis = "flu"
        doctors = DoctorModel.objects.filter(
            patients__medical_records__diagnoses__icontains=specific_diagnosis
        ).distinct()
        print([d.name for d in doctors])

        # 3 Find all patients treated by a particular nurse.
        nurse_id = 16
        patients = PatientModel.objects.filter(nurse_id=nurse_id)
        print([p.name for p in patients])

        # 4 Retrieve the contact number of the doctor for a given patient.
        patient_id = 7
        doctor_contacts = DoctorModel.objects.filter(patients__id=patient_id).values_list("contact_number", flat=True)
        print(list(doctor_contacts))

        # 5 Get the total number of patients admitted to the hospital.
        admitted_patient = PatientModel.objects.count()
        print(admitted_patient)

        # 6 Find the patients who are not assigned to any nurse.
        patients = PatientModel.objects.filter(nurse__isnull=True)
        print([p.name for p in patients])

        # 7 Retrieve the names of nurses who have patients with a specific prescription.
        prescription = "paracetamol"
        nurses = NurseModel.objects.filter(
            patients__medical_records__precription__icontains=prescription
        ).distinct()
        print([n.name for n in nurses])

        # 8 Get the average age of patients in the hospital.
        avg_age = PatientModel.objects.aggregate(Avg("age"))
        print(avg_age["age__avg"])

        # 9 Find the most recently admitted patient.
        latest_patient = PatientModel.objects.latest("date_admitted")
        print(latest_patient.name)

        # 10 Retrieve all doctors who have more than five patients.
        doctors = DoctorModel.objects.annotate(num_patients=Count("patients")).filter(num_patients__gt=5)
        print([d.name for d in doctors])

        # 11 Find the patients who have been admitted for more than a week.
        week_ago = timezone.now() - timedelta(days=7)
        patients = PatientModel.objects.filter(date_admitted__lt=week_ago)
        print([p.name for p in patients])

        # 12 Get the number of patients assigned to each nurse.
        nurse_patient_count = NurseModel.objects.annotate(num_patients=Count("patients"))
        print(list(nurse_patient_count.values_list("name", "num_patients")))

        # 13 Retrieve the names of patients who have a specific doctor.
        doctor_id = 1
        patients = PatientModel.objects.filter(doctors__id=doctor_id)
        print([p.name for p in patients])

        # 14 Find the doctors who specialize in a specific medical field.
        field = "Mudlogger"
        doctors = DoctorModel.objects.filter(specialization__icontains=field)
        print([d.name for d in doctors])

        # 15 Get the names of patients treated by a doctor with a specific specialization.
        specialization = "Cardiology"
        patients = PatientModel.objects.filter(doctors__specialization__icontains=specialization).distinct()
        print([p.name for p in patients])

        # 16 Find the nurses who have not been assigned any patients.
        nurses = NurseModel.objects.filter(patients__isnull=True)
        print([n.name for n in nurses])

        # 17 Retrieve the latest medical record for a given patient.
        patient_id = 1
        latest_record = MedicalRecord.objects.filter(patient_id=patient_id).latest("id")
        print(latest_record.diagnoses)

        # 18 Get the names of patients with a specific diagnosis.
        diagnosis = "flu"
        patients = PatientModel.objects.filter(medical_records__diagnoses__icontains=diagnosis).distinct()
        print([p.name for p in patients])

        # 19 Find the doctors who have patients of a certain age group.
        min_age, max_age = 20, 30
        doctors = DoctorModel.objects.filter(patients__age__range=(min_age, max_age)).distinct()
        print([d.name for d in doctors])

        # 20 Find the nurses who have patients with a specific age.
        nurses = NurseModel.objects.filter(patients__age=25).distinct()
        print([n.name for n in nurses])

        # 21 Get the total number of medical records in the system.
        mr = MedicalRecord.objects.count()
        print(mr)

        # 22 Retrieve the names of patients treated by a nurse with a specific contact number.
        contact = "333300"
        patients = PatientModel.objects.filter(nurse__contact_number=contact)
        print([p.name for p in patients])

        # 23 Find the patients who are treated by more than one doctor.
        patients = PatientModel.objects.annotate(num_doctors=Count("doctors")).filter(num_doctors__gt=1)
        print([p.name for p in patients])

        # 24 Find the names of doctors who have treated patients with a specific prescription.
        prescription = "paracetamol"
        doctors = DoctorModel.objects.filter(
            patients__medical_records__precription__icontains=prescription
        ).distinct()
        print([d.name for d in doctors])

        # 25 Get the average age of patients treated by each doctor.
        avg_age_per_doctor = DoctorModel.objects.annotate(avg_age=Avg("patients__age"))
        print([(d.name, d.avg_age) for d in avg_age_per_doctor])

        # 26 Find the patients who have not been assigned to any doctor.
        patients = PatientModel.objects.annotate(num_doctors=Count("doctors")).filter(num_doctors=0)
        print([p.name for p in patients])

        # 27 Retrieve the doctors who have patients admitted on a specific date.
        specific_date = timezone.now().date()
        doctors = DoctorModel.objects.filter(patients__date_admitted__date=specific_date).distinct()
        print([d.name for d in doctors])

        # # 28 Get the number of patients admitted each month.
        # monthly = PatientModel.objects.annotate(month=timezone.ExtractMonth("date_admitted")).values("month").annotate(total=Count("id"))
        # print(list(monthly))

        # 29 Find the patients with the highest age in the hospital.
        eldest = PatientModel.objects.order_by("-age").first()
        print(eldest.name)

        # 30 Retrieve all nurses who have patients admitted on a specific date.
        nurses = NurseModel.objects.filter(patients__date_admitted__date=specific_date).distinct()
        print([n.name for n in nurses])

        # 31 Find the doctors who have patients with a specific age.
        doctors = DoctorModel.objects.filter(patients__age=40).distinct()
        print([d.name for d in doctors])

        # 32 Get the number of patients treated by each doctor.
        doctors = DoctorModel.objects.annotate(num_patients=Count("patients"))
        print([(d.name, d.num_patients) for d in doctors])

        # 33 Retrieve the names of patients with a specific age.
        patients = PatientModel.objects.filter(age=30)
        print([p.name for p in patients])

        # 34 Find the nurses who have patients with a specific diagnosis.
        nurses = NurseModel.objects.filter(patients__medical_records__diagnoses__icontains="cough").distinct()
        print([n.name for n in nurses])

        # 35 Get the names of patients treated by a nurse with a specific contact number.
        contact_number = "123-456-7890"
        patients = PatientModel.objects.filter(nurse__contact_number=contact_number)
        print([p.name for p in patients])

        # 36 Find the doctors who have not been assigned any patients.
        doctors = DoctorModel.objects.filter(patients__isnull=True)
        print([d.name for d in doctors])

        # 37 Retrieve the patients who have medical records with a specific prescription.
        patients = PatientModel.objects.filter(medical_records__precription__icontains="panadol").distinct()
        print([p.name for p in patients])

        # 38 Get the average age of patients treated by each doctor.
        doctors = DoctorModel.objects.annotate(avg_age=Avg("patients__age"))
        print([(d.name, d.avg_age) for d in doctors])

        # 39 Find the doctors who have patients with a specific prescription.
        prescription = "paracetamol"
        doctors = DoctorModel.objects.filter(
            patients__medical_records__precription__icontains=prescription
        ).distinct()
        print([d.name for d in doctors])

        # 40 Retrieve the names of patients treated by a doctor with a specific contact number.
        patients = PatientModel.objects.filter(doctors__contact_number="123-456-7890")
        print([p.name for p in patients])

        # 41 Find the nurses who have patients with a specific prescription.
        nurses = NurseModel.objects.filter(
            patients__medical_records__precription__icontains="panadol"
        ).distinct()
        print([n.name for n in nurses])

        # 42 Get the total number of patients treated by nurses in a specific specialization.
        total = PatientModel.objects.filter(doctors__specialization__icontains="Cardiology").count()
        print(total)

        # 43 Retrieve the patients who have not been assigned to any nurse.
        patients = PatientModel.objects.filter(nurse__isnull=True)
        print([p.name for p in patients])

        # 44 Find the doctors who have patients admitted for more than a week.
        week_ago = timezone.now() - timedelta(days=7)
        doctors = DoctorModel.objects.filter(patients__date_admitted__lt=week_ago).distinct()
        print([d.name for d in doctors])

        # 45 Get the names of patients with a specific diagnosis treated by a specific doctor.
        patients = PatientModel.objects.filter(
            doctors__id=1,
            medical_records__diagnoses__icontains="flu"
        ).distinct()
        print([p.name for p in patients])

        # 46 Find the nurses who have patients with a specific age group.
        nurses = NurseModel.objects.filter(patients__age__range=(18, 30)).distinct()
        print([n.name for n in nurses])

        # 47 Retrieve the doctors who have patients with a specific diagnosis and age group.
        doctors = DoctorModel.objects.filter(
            patients__medical_records__diagnoses__icontains="flu",
            patients__age__range=(20, 40)
        ).distinct()
        print([d.name for d in doctors])

        # 48 Get the number of patients treated by each nurse in a specific specialization.
        result = NurseModel.objects.annotate(
            count=Count("patients", filter=models.Q(patients__doctors__specialization__icontains="Cardiology"), distinct=True)
        ).values_list("name", "count")
        print(list(result))

        # 49 Find the patients who have been treated by more than one nurse.
        # (assuming hospitalmodel tracking nurses)
        patients = PatientModel.objects.annotate(
            num_nurses=Count("hospital_patients__nurse", distinct=True)
        ).filter(num_nurses__gt=1)
        print([p.name for p in patients])

        # 50 Retrieve the names of doctors who have patients with a specific diagnosis and age group.
        doctors = DoctorModel.objects.filter(
            patients__medical_records__diagnoses__icontains="flu",
            patients__age__range=(20, 40)
        ).distinct()
        print([d.name for d in doctors])

        # ----------------------------- Task-2 Queries -----------------------------

        # 1 Select all patients with their associated doctors and nurses.
        patients = PatientModel.objects.select_related("nurse").prefetch_related("doctors")
        print(patients)

        # 2 Select all patients admitted after a specific date.
        date = timezone.now() - timedelta(days=30)
        patients = PatientModel.objects.filter(date_admitted__gt=date)
        print([p.name for p in patients])

        # 3 Count the total number of patients.
        total = PatientModel.objects.count()
        print(total)

        # 4 Count the total number of patients with a specific age.
        age = 30
        count = PatientModel.objects.filter(age=age).count()
        print(count)

        # 5 Select all patients with their associated doctors and nurses prefetched.
        patients = PatientModel.objects.select_related("nurse").prefetch_related("doctors")
        print(patients)

        # 6 Count the total number of doctors associated with each patient.
        patients = PatientModel.objects.annotate(num_doctors=Count("doctors"))
        print([(p.name, p.num_doctors) for p in patients])

        # 7 Sum the ages of all patients.
        total_age = PatientModel.objects.aggregate(total=Count("age"))
        print(total_age["total"])

        # 8 Select all patients along with the number of doctors associated with each.
        patients = PatientModel.objects.annotate(num_doctors=Count("doctors"))
        print([(p.name, p.num_doctors) for p in patients])

        # 9 Select all patients along with their medical records, if available.
        patients = PatientModel.objects.prefetch_related("medical_records")
        print(patients)

        # 10 Count the total number of nurses associated with each patient.
        pts = PatientModel.objects.annotate(num_nurses=Count("nurse"))
        print([(p.name, p.num_nurses) for p in pts])

        # 11 Select all patients with their associated nurses and the nurses' contact numbers.
        pts = PatientModel.objects.select_related("nurse")
        print([(p.name, p.nurse.name, p.nurse.contact_number) for p in pts])

        # 12 Select all patients along with the total number of medical records for each.
        pts = PatientModel.objects.annotate(num_records=Count("medical_records"))
        print([(p.name, p.num_records) for p in pts])

        # 13 Select all patients with their diagnoses and prescriptions, if available.
        pts = PatientModel.objects.prefetch_related("medical_records")
        for p in pts:
            print(p.name, [(rec.diagnoses, rec.precription) for rec in p.medical_records.all()])

        # 14 Count the total number of patients admitted in a specific year.
        year = timezone.now().year
        print(PatientModel.objects.filter(date_admitted__year=year).count())

        # 15 Select all patients along with their doctors' specializations.
        pts = PatientModel.objects.prefetch_related("doctors")
        for p in pts:
            print(p.name, [d.specialization for d in p.doctors.all()])

        # 16 Select all patients along with the count of medical records for each.
        pts = PatientModel.objects.annotate(num=Count("medical_records"))
        print([(p.name, p.num) for p in pts])

        # 17 Select all doctors with the count of patients they are associated with.
        docs = DoctorModel.objects.annotate(num=Count("patients"))
        print([(d.name, d.num) for d in docs])

        # 18 Select all patients along with the count of nurses they are associated with.
        pts = PatientModel.objects.annotate(num=Count("nurse"))
        print([(p.name, p.num) for p in pts])

        # 19 Annotate the average age of patients.
        print(PatientModel.objects.aggregate(avg=Avg("age"))["avg"])

        # 20 Annotate the maximum age of patients.
        print(PatientModel.objects.aggregate(Max("age"))["age__max"])

        # 21 Annotate the minimum age of patients.
        print(PatientModel.objects.aggregate(Min("age"))["age__min"])

        # 22 Select all patients along with the earliest admission date.
        pts = PatientModel.objects.earliest("date_admitted")
        print(pts.name)

        # 23 Select all doctors with their associated patients prefetched.
        docs = DoctorModel.objects.prefetch_related("patients")
        print(docs)

        # 24 Select all nurses with their associated patients prefetched.
        ns = NurseModel.objects.prefetch_related("patients")
        print(ns)

        # 25 Select all patients along with the count of distinct doctors they are associated with.
        pts = PatientModel.objects.annotate(num=Count("doctors", distinct=True))
        print([(p.name, p.num) for p in pts])
