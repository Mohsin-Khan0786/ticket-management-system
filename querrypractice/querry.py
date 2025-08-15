# 1 create()
# d1=DoctorModel.objects.create(name="Dr Ali",specialization="Cardiology" ,contact_number="000111")
#  2 all()
# *DoctorModel.objects.all()
# *HospitalModel.objects.all()
# *NurseModel.objects.all()
# 4 Diference between  object and query set
# *get()
# doctors = DoctorModel.objects.get(id=1)
#  print(doctors)
# Dr Ali
#* filter()
# doctors = DoctorModel.objects.filter(specialization="Cardiology")
#  print(doctors)
# <QuerySet [<DoctorModel: Dr Ali>, <DoctorModel: Dr Ali>]>
#5 get()
#DoctorModel.objects.get(name="Dr. Ali")
#6 filter()
# PatientModel.objects.filter(nurse__name="Nurse Fatima")
# 7 is __null
# PatientModel.objects.filter(nurse__isnull=True)
# 8 lte/gte
# PatientModel.objects.filter(age__lte=30)
# PatientModel.objects.filter(age__gte=30)
# 9 exists()
# PatientModel.objects.filter(age__gte=60).exists()
# 10 count()
# DoctorModel.objects.count()
#11 exclude()
# PatientModel.objects.exclude(age__lte=18)
# 12 select_related & prefetch_related
# PatientModel.objects.select_related('nurse').all()
# PatientModel.objects.prefetch_related('doctors').all()
# 13 Update and delete
#DoctorModel.objects.filter(id=1).update(specialization='oncologist')
# DoctorModel.objects.get(id=4).delete()
# 14 bulk_create
# DoctorModel.objects.bulk_create([
#     DoctorModel(name="Dr SamiUllah", specialization="peadtrics", contact_number="03123456789"),
#     DoctorModel(name="Dr Ammara", specialization="Radiology", contact_number="0301983746557"])
# )
# 15 bulk_update
# DoctorModel.objects.bulk_update(
#     [DoctorModel(id=1, specialization="Neurology")],
#     ['specialization']
# )
# 16  get_or_create /update_or_create
# DoctorModel.objects.get_or_create(
#     name="Dr. Ali", defaults={"specialization": "Cardiology", "contact_number": "03001234567"}
# )
# DoctorModel.objects.update_or_create(
#     name="Dr. Ali", defaults={"specialization": "Orthopedic"}
# )
# 17 order_by
# PatientModel.objects.order_by('-age')  