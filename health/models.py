from datetime import datetime, timedelta
from distutils.command import upload
from email import message
from math import remainder
from sys import maxsize
from xml.parsers.expat import model
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_celery_beat.models import MINUTES, PeriodicTask, CrontabSchedule, PeriodicTasks
from django.urls import reverse
import json
# Create your models here.
class Profile(models.Model):
    patient=models.OneToOneField(User,on_delete=models.CASCADE)
    p_id=models.CharField(max_length=12,null=True)
    username = models.CharField(max_length=12, null=True)
    email = models.EmailField(max_length=20, null=True)
    phone = models.PositiveBigIntegerField(null=True)
    fname = models.CharField(max_length=20, null=True)
    lname = models.CharField(max_length=20, null=True)
    age = models.IntegerField(null=True)
    sex=models.CharField(max_length=10)
    dob=models.DateField(default=datetime.today)
    height = models.FloatField( null=True)
    weight = models.FloatField( null=True)
    breakfast = models.TimeField(null=True)
    lunch = models.TimeField(null=True)
    dinner = models.TimeField(null=True)
    blood_grp = models.CharField(max_length=10, null=True)

    def __str__(self):
        return self.patient.username
    def dash_url(self):
        return reverse('patient-dash', kwargs={'patient_id': self.p_id})
    def bmi(self):
        BMI = self.weight / (self.height/100)**2
        return round(BMI,2)
    
    #checkup id genration
    def get_checkup_id(self):
        checkup=self.checkups.all()
        checkup_count=checkup.count()
        checkup_id='CHKUP'+str(checkup_count)
        return checkup_id

#class Doctor(models.Model):
#class Checkup
#class disease
#class mental_health


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    phone = models.PositiveBigIntegerField(null=True)
    specialization = models.CharField(max_length=20, null=True)
    doctor_id = models.CharField(max_length=12, null=True)
    works_in = models.CharField(max_length=12, null=True)
    sex = models.CharField(max_length=12, null=True)


class Medicines(models.Model):
    timeslots=(('BREAK FAST',1),
                    ('LUNCH',2),
                    ('DINNER',3)
              )
    med_type=(('PILLS','PILLS'),
              ('TABLET','TABLET'),
              ('INJECTION','INJECTION'),
              ('SYRUP','SYRUP'))
    medicine_name = models.CharField(max_length=100)
    medicine_type=models.CharField(max_length=30,choices=med_type,default='PILLS')
    dosage=models.FloatField(default=0)
    before_food=models.BooleanField(default=True)
    after_food=models.BooleanField(default= False)
    time_slot = models.CharField(choices=timeslots, max_length=20)

class medicine_prescription(models.Model):
    timeslots = (('BREAK FAST', 1),
                 ('LUNCH', 2),
                 ('DINNER', 3)
                 )
    intake_user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    medicines = models.ManyToManyField(Medicines)
    timeslot = models.CharField(choices=timeslots, default=1, max_length=20)
    before_food = models.BooleanField(default=True)
    send_on=models.DateTimeField()
    message = models.TextField(max_length=200, default='Its Time to take your medicine')


@receiver(post_save, sender=medicine_prescription)
def notification_handler(sender, instance, created, **kwargs):
    # call group_send function directly to send notificatoions or you can create a dynamic task in celery beat
    if created:
        if instance.before_food:
            send_time=instance.send_on - timedelta(minutes=30)
            name=f"medicine-notification-{instance.intake_user.p_id}-{instance.timeslot}-BF"
        else:
            send_time = instance.send_on + timedelta(minutes=30)
            name = f"medicine-notification-{instance.intake_user.p_id}-{instance.timeslot}-BF"

        schedule, created = CrontabSchedule.objects.get_or_create(hour=send_time.hour, minute=send_time.minute)
        task = PeriodicTask.objects.create(crontab=schedule, name=name, task="notifications.tasks.medicine_notification", args=json.dumps((instance.id,)))


class track_medicine(models.Model):
    prescription = models.ForeignKey(medicine_prescription, on_delete=models.CASCADE, related_name="track_medicine")
    medicine_date=models.DateField()
    took_medicines = models.BooleanField(default=False)
    reminder_sent = models.BooleanField(default=False)
    class meta:
        ordering=['-medicine_date']

class Trackweight(models.Model):
    current_weight=models.FloatField()
    user=models.ForeignKey(Profile,on_delete=models.CASCADE)
    timestamp=models.DateTimeField()


class symptoms(models.Model):
    symptom_name=models.CharField(max_length=100,null=False)
    symptom_desc=models.CharField(max_length=500,null=True)

    def __str__(self):
        return self.symptom_name

class Usersymptoms(models.Model):
    check_up_id=models.CharField(max_length=20,null=False)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    my_symptoms=models.ManyToManyField(symptoms)
    timestamp=models.TimeField(default=datetime.now)

class Checkup(models.Model):
    types=(('DIABETES','DIABETES'),
            ('HEART DISEASE','HEART DISEASE'),
            ('SYMPTOMS CHECK','SYMPTOMS CHECK'))
    checkup_id=models.CharField(max_length=12)
    checkup_user=models.ForeignKey(Profile,on_delete=models.CASCADE,related_name="checkups")
    checkup_date=models.DateTimeField()
    checkup_type=models.CharField(max_length=20,choices=types)
    checkup_details=models.JSONField(null=True)
    is_verified = models.BooleanField(default=False)
    scan_path = models.ImageField(upload_to='ecg scan',null=True)
    verified_by = models.ForeignKey(Doctor, on_delete=models.CASCADE,null=True)


class Report(models.Model):
    pdf_path=models.CharField(max_length=12)
    generated_on=models.DateTimeField()
    generates=models.OneToOneField(Checkup,on_delete=models.CASCADE) 




    
'''class Disease_prediction(models.Model):
    checkup_id=models.CharField(max_length=12)
    predictor_type=models.CharField(max_length=12)
    is_verified=models.CharField(max_length=12)
    scan_path=models.CharField(max_length=12)
    prediction=models.CharField(max_length=12)
    name_patient=models.ForeignKey(Profile,on_delete=models.CASCADE)
    verified_by=models.ForeignKey(Doctor,on_delete=models.CASCADE)'''


class Mental_health(models.Model):
    intent=models.CharField(max_length=12)
    suggestion=models.CharField(max_length=12)
    score=models.CharField(max_length=12)
    analyse=models.ForeignKey(Profile,on_delete=models.CASCADE)


'''class predict_diabetes(models.Model):
    Glucoselevel=models.CharField(max_length=12)
    Insulin=models.CharField(max_length=12)
    BMI=models.CharField(max_length=12)
    DiabetesPF=models.CharField(max_length=12)
    Age=models.CharField(max_length=12)'''
