from django.urls import path
from . import views

#from .utilis import update_symptoms

urlpatterns = [
    path('chat-bot', views.chat_bot, name='chat_bot'),
    path('predict', views.predict, name='predict'),
    path('home',views.home,name='home'),
<<<<<<< HEAD
    path('diabetes-prediction',views.predict_diabetes,name='predicteddiabetes')
=======
    path('diabetes-predict', views.diabetes_view, name='diabetes-predict'),
    path('diabetes-result', views.diabetes, name='predicteddiabetes')
>>>>>>> 3b2a24de038250cb3a9027b701717d074fb8e296

    #path('save-symp',update_symptoms,name='symptoms-update'),
]

