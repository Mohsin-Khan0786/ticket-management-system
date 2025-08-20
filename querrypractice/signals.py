from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PatientModel, NotificationModel
from django.utils.timezone import now

@receiver(post_save, sender=PatientModel)
def create_patient_notification(sender, instance, created, **kwargs):
    if created:  
        doctor_name = instance.doctors.name
        nurse_name = instance.nurse.name
        patient_name = instance.name
        time = now().strftime("%Y-%m-%d %H:%M:%S")

        message = f"Dr {doctor_name} and Nurse {nurse_name} has been assigned a new patient {patient_name} at {time}"
        NotificationModel.objects.create(message=message)
