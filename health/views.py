from cmath import e
from datetime import datetime
from errno import EEXIST
from multiprocessing import context
from unicodedata import name
from unittest import result
from django.contrib.auth.decorators import login_required
from ast import Return
from asyncio.windows_events import NULL
from cgitb import text
from email.mime import message
import json
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .utilis import get_intent,symptoms,predict_disease,precautionDictionary,description, predict_diabetes
from healthApp.randgenerator import rand
from .models import Checkup, Profile, Usersymptoms,symptoms as Symptoms
import pickle
from .pedigree import Pedigree
from .Ecg import  ECG
from django.template.loader import get_template
from io import BytesIO
from xhtml2pdf import pisa
import os

#intialize ecg object

#from .models import predict_diabetes

# Create your views here.

@login_required
def chat_bot(request):
    return render(request,'chat-bot.html')

def home(request):
    content={"name":"devu","symptoms":symptoms}
    return render(request, 'healthica/homepage.html',content)
    #return HttpResponse('<h1>hello</h1>')

def dashboard_patient(request,patient_id):
    patient=Profile.objects.get(p_id=patient_id)
    context={
        'patient_id':patient.p_id,
        'patient':patient
    }
    
    return render(request,"dashboard-patient.html",context)

def create_checkup(request,details,type):
    patient=Profile.objects.get(patient=request.user)
    details=json.dumps(details)
    chkup_id=patient.get_checkup_id()
    if type=='HEART DISEASE':
        image=request.FILES['ecg']
        checkup = Checkup(checkup_id=chkup_id, checkup_user=patient, checkup_date=datetime.now(
        ), checkup_details=details, checkup_type=type,scan_path=image)
        checkup.save()
        return checkup
    checkup=Checkup(checkup_id=chkup_id,checkup_user=patient,checkup_date=datetime.now(),checkup_details=details,checkup_type=type)
    checkup.save()
    return checkup

def get_response(request,intent,session):
    response=''
    print(intent)
    try:
        user_symptoms = Usersymptoms.objects.get(check_up_id=session["checkup_ID"])
    except Usersymptoms.DoesNotExist:
        user_symptoms = Usersymptoms(user=request.user,check_up_id=rand(6))
        user_symptoms.save()
    if intent == "greeting":
        response = 'Hey {}, what symptoms do you have? please enter one of your symptoms.(Ex. headache, vomiting etc.)'.format(request.user.first_name)
    elif intent == "ask_symptoms":
        try:
            main_symp=Symptoms.objects.get(symptom_name=session["message"])
            user_symptoms.my_symptoms.add(main_symp)
        except Symptoms.DoesNotExist:
            response='Please Enter correct Symptoms!'
            return response,session["checkup_ID"]
        response = "Enter one more symptom beside {}. (Enter 'No' if not)".format(session["message"])
    elif intent == "ask_symptoms-no":
        affected_symtoms=[]
        final_symptoms=[]
        for i in range(len(symptoms)):
            affected_symtoms.append(0)
        for i in range(user_symptoms.my_symptoms.count()):
            print(user_symptoms.my_symptoms.all()[1])
            affected_symtoms[symptoms.index(user_symptoms.my_symptoms.all()[i].symptom_name)]=1
            final_symptoms.append(
                user_symptoms.my_symptoms.all()[i].symptom_name)
        disease=predict_disease(affected_symtoms,final_symptoms)
        print(affected_symtoms,final_symptoms)
        response=["disease","You may have {} disease".format(disease),disease]

    elif intent == "end-chat":
        response = ''
    else:
        response='Invalid Message!'
    return response,user_symptoms.check_up_id


@csrf_exempt
def predict(request):
    text = json.loads(request.body)
    msg = text["message"]
    intent=get_intent(msg)
    res,checkupid=get_response(request,intent,text)
    if(res[0]=="disease"):
        message = {"reply": res[1], "checkup_ID": checkupid}
        user_symptoms = Usersymptoms.objects.get(check_up_id=checkupid)
        details={'symptoms':[item.symptom_name for item in user_symptoms.my_symptoms.all()],'result':res[1]}
        create_checkup(request, details, 'SYMPTOMS CHECK')
    else:
        message={"reply":res,"checkup_ID":checkupid}
    return HttpResponse(json.dumps(message), content_type='application/json')




def diabetes_view(request):
    return render(request, 'diabeticform.html',{'age':request.user.profile.age})

@login_required
def diabetes(request):
    if request.method=="POST":
        Glucoselevel=request.POST.get('Glucose Level')
        Insulin=request.POST.get('Insulin')
        bmi=request.POST.get('BMI')
        DiabetesPF=request.POST.get('Diabetes PF')
        Age=request.POST.get('Age')
        r,pred=predict_diabetes(request)#)
        details = {key:x for key, x in request.POST.items() if key != "csrfmiddlewaretoken"}
        if pred==1:
            result = "Chances of having Diabetes is more."
        else:
            result = "No Worries!!! You don't have Diabetes."
        details["results"]=result
        create_checkup(request, details, 'DIABETES')
        return r
        #en.save()
        #return render(request,'result.html'



def heartdisease(request):

    #get the uploaded image
    if request.method=='POST':
        #intialize ecg object
        ecg = ECG()
        #get the uploaded image
        uploaded_file = request.FILES['ecg']
        if uploaded_file is not None:
            """#### **UPLOADED IMAGE**"""
            # call the getimage method
            ecg_user_image_read = ecg.getImage(uploaded_file)
            #show the image
            

            """#### **GRAY SCALE IMAGE**"""
            #call the convert Grayscale image method
            ecg_user_gray_image_read = ecg.GrayImgae(ecg_user_image_read)
            
            
            
            """#### **DIVIDING LEADS**"""
            #call the Divide leads method
            dividing_leads=ecg.DividingLeads(ecg_user_image_read)

            
            
            """#### **PREPROCESSED LEADS**"""
            #call the preprocessed leads method
            ecg_preprocessed_leads = ecg.PreprocessingLeads(dividing_leads)

        
            
            """#### **EXTRACTING SIGNALS(1-12)**"""
            #call the sognal extraction method
            ec_signal_extraction = ecg.SignalExtraction_Scaling(dividing_leads)
            
            """#### **CONVERTING TO 1D SIGNAL**"""
            #call the combine and conver to 1D signal method
            ecg_1dsignal = ecg.CombineConvert1Dsignal()
            
                
            """#### **PERFORM DIMENSINALITY REDUCTION**"""
            #call the dimensinality reduction funciton
            ecg_final = ecg.DimensionalReduciton(ecg_1dsignal)
            
            
            """#### **PASS TO PRETRAINED ML MODEL FOR PREDICTION**"""
            #call the Pretrainsed ML model for prediction
            ecg_model=ecg.ModelLoad_predict(ecg_final)
            details={'result':ecg_model}
            create_checkup(request, details, 'HEART DISEASE')
            return render(request,'heartdisease.html',{'prediction':ecg_model})
    else:
        return render(request,'heartdisease.html')


@csrf_exempt
def pedigree(request):
    data = json.loads(request.body)
    for keys,vals in data.items():
        if vals=="yes":
            data[keys]=True
        else:
            data[keys]=False
    #print(data)
    p = Pedigree(data["grandp_f"], data["grandp_m"], data["diabetic_father"], data["diabetic_mother"],
                 request.user.profile.sex.upper(), data["siblings"])
    p.get_parent_chromosomes()
    p.offsprings = p.punnet_square('disease-allele')
    p.has_diabetic_siblings()
    p.offsprings_xlinked = p.punnet_square('x-linked')
    p.determine_type_probab()
    p.x_linked_probablity()

    pedigree={"pedigree":p.probablity}
    return HttpResponse(json.dumps(pedigree), content_type='application/json')



def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)#, link_callback=fetch_resources)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None



def PDF(request):

    data = {
            'name': "Devu",
            'disease': "heartdisease" ,
            'email': "devubalakrishnan@yahoo.com",
            'date':"12/3/22" ,
        
        }
    pdf = render_to_pdf('reportpdf.html', data)

    if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "reportpdf_%s.pdf" %(data['name'])
            content = "inline; filename='%s'" %(filename)
            #download = request.GET.get("download")
            #if download:
            content = "attachment; filename=%s" %(filename)
            response['Content-Disposition'] = content
            return response
    return HttpResponse("Not found")


 






