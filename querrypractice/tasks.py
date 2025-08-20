from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import PatientModel

@shared_task
def remove_old_patients():
    one_hour_ago = timezone.now() - timedelta(hours=1)
    old_patients = PatientModel.objects.filter(date_admitted__lt=one_hour_ago)
    count=old_patients.count()
    old_patients.delete()
    return(f"{count} patients deleted who were admitted more than 1 hour ago.")

@shared_task
def patient_summary_last_30_mins():
    thirty_mins_ago = timezone.now() - timedelta(minutes=30)

    recent_patients = PatientModel.objects.filter(
        date_admitted__gte=thirty_mins_ago
    ).prefetch_related('medical_records')

    summary = []

    for patient in recent_patients:

        record_details = [

            f"Diagnosis: {record.diagnoses}, Prescription: {record.precription}"

            for record in patient.medical_records.all()
        ]
        if not record_details:

            record_details = ["No medical record available"]

        summary.append(

            f"{patient.name} admitted at {patient.date_admitted.strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"Medical Records: {' | '.join(record_details)}"
        )

    print("Summary of patients admitted in last 30 mins:")
    for line in summary:
        print(line)

    return summary
