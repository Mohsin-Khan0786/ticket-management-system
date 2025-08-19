from celery.schedules import crontab
CELERY_BEAT_SCHEDULE = {
    'remove-old-patients-every-hour': {
        'task': 'querrypractice.tasks.remove_old_patients',
        'schedule': crontab(minute=0),
    },
    'patient-summary-every-30-min': {
        'task': 'querrypractice.tasks.patient_summary_last_30_mins', 
        'schedule': crontab(minute='*/30'),
    },
}