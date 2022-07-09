from django.contrib import admin
from .models import symptoms,Usersymptoms,Doctor,Profile
# Register your models here.


class symptomsad(admin.ModelAdmin):
    list_display = ('pk','symptom_name')

class usersymp_ad(admin.ModelAdmin):
    list_display=('pk','check_up_id','user')


class doctor_ad(admin.ModelAdmin):
    list_display = ('pk', 'doctor_id', 'user')


class patient_ad(admin.ModelAdmin):
    list_display = ('pk', 'p_id', 'patient')
admin.site.register(Doctor,doctor_ad)
admin.site.register(symptoms,symptomsad)
admin.site.register(Usersymptoms,usersymp_ad)
admin.site.register(Profile,patient_ad)
