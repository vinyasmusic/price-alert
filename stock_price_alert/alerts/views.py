import json
import logging
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Alert
from .serializers import AlertSerializer

logging.basicConfig(filename='alerts.log',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.INFO)
log = logging.getLogger(__name__)


@login_required()
def view_alerts(request):
    alerts = Alert.objects.filter(user=request.user).order_by('scrip_symbol')
    # helper.template = 'bootstrap/table_inline_formset.html'

    return render(request, 'alerts/set_alerts.html', {'alerts': alerts})


@login_required
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def add_alerts(request):
    data = list(request.data)
    error_message = None
    for datum in data:
        print(datum)
        if datum.get('uuid', None):
            alert_obj = Alert.objects.get(uuid=datum['uuid'])
            alert_serializer = AlertSerializer(alert_obj, data=datum)
        else:
            alert_serializer = AlertSerializer(data=datum)

        if alert_serializer.is_valid():
            alert_serializer.save()
        else:
            log.exception(alert_serializer.errors)
            error_message = alert_serializer.error_messages
            log.exception(alert_serializer.error_messages)
    if error_message:
        return Response({'message': error_message}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'message': 'Success'}, status=status.HTTP_200_OK)
