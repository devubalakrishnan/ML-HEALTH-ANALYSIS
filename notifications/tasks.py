from ast import Try
import asyncio
import json
from math import remainder
from celery import shared_task,Celery,states
from healthApp import settings
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from health.models import medicine_prescription,track_medicine
from celery.exceptions import Ignore



@shared_task(bind=True)
def medicine_notification(self,data):
    
    try:
        prescription=medicine_prescription.objects.filter(id=int(data))
        if len(prescription)>0:
            prescription=prescription.first()
            userid = prescription.intake_user.p_id
            channel_layer=get_channel_layer()
            channel_name="medicine-notificaton-%s"%userid
            loop=asyncio.new_event_loop()
            loop.run_until_complete(channel_layer.group_send(
                channel_name,
                {
                    'type': 'send_medicine_notification',
                    'message': json.dumps(prescription.message)
                }
            ))
            track_medicine(prescription=prescription,medicine_date=prescription.send_on.date(),reminder_sent=True).save()
            #prescription.save()
            return "Done"
        else:
            self.update_state(
                state='FAILURE',
                meta={'exe':'Not Found'}
            )
            raise Ignore()
    except:
        self.update_state(
            state='FAILURE',
            meta={'exe': 'Failed'}
        )
        raise Ignore()

