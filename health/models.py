from datetime import datetime
from sys import maxsize
from xml.parsers.expat import model
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
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

#class Doctor(models.Model):
#class Checkup
#class disease
#class mental_health

class Medicines(models.Model):
    intake_user=models.ForeignKey(Profile,on_delete=models.CASCADE)
    medicine_name = models.CharField(max_length=100)
    before_food=models.BooleanField(default=True)
    after_food=models.BooleanField(default= False)
    time_slot=models.PositiveSmallIntegerField(default =1)
    
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
    checkup_id=models.CharField(max_length=12)
    checkup_user=models.ForeignKey(Profile,on_delete=models.CASCADE)
    checkup_date=models.DateTimeField()
    checkup_type=models.CharField(max_length=12)



class Report(models.Model):
    pdf_path=models.CharField(max_length=12)
    generated_on=models.DateTimeField()
    generates=models.OneToOneField(Checkup,on_delete=models.CASCADE) 


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True)
    phone = models.PositiveBigIntegerField(null=True)
    specialization = models.CharField(max_length=20, null=True)
    doctor_id = models.CharField(max_length=12, null=True)
    works_in = models.CharField(max_length=12, null=True)
    sex = models.CharField(max_length=12, null=True)

    
class Disease_prediction(models.Model):
    checkup_id=models.CharField(max_length=12)
    predictor_type=models.CharField(max_length=12)
    is_verified=models.CharField(max_length=12)
    scan_path=models.CharField(max_length=12)
    prediction=models.CharField(max_length=12)
    name_patient=models.ForeignKey(Profile,on_delete=models.CASCADE)
    verified_by=models.ForeignKey(Doctor,on_delete=models.CASCADE)


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
