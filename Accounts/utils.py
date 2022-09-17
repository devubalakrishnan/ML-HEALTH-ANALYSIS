from django.contrib.auth.models import User

def get_IDs():
    querry=User.objects.all().order_by('pk').last()
    current_pk=querry.pk+1
    num=10000+current_pk
    D_id = 'DR'+str(num)
    P_id = 'PT'+str(num)
    return D_id,P_id
