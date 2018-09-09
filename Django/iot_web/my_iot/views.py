from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import requests as rts

from django.conf import settings

from my_iot.models import HistoryValue

def getValue():
    t = ''
    h = ''
    if settings.CURRENT_TEMPERATURE == None:
        t = "无读数"
    else:
        t = str(settings.CURRENT_TEMPERATURE)
    if settings.CURRENT_HUMIDITY == None:
        h = "无读数"
    else:
        h = str(settings.CURRENT_HUMIDITY)
    return t, h

def index(request):
    t, h = getValue()
    return render(request, 'my_iot/index.html', {'t':t, 'h':h})

@csrf_exempt
def data(request):
    if 'data' in request.GET:
        d = json.loads(request.GET['data'].replace("'", '"'))
        print("get data {0}, {1}".format(d['t'], d['h']))
        value = HistoryValue(temperature=d['t'], humidity=d['h'])
        value.save()
        settings.CURRENT_TEMPERATURE = d['t']
        settings.CURRENT_HUMIDITY = d['h']
    if 'get' in request.GET:
        rts.get("http://192.168.137.49:5000" + "?op=" + request.GET['get'])
    if 'recv' in request.GET:
        t, h = getValue()
        return HttpResponse(json.dumps({'t':t, 'h': h}))
    return HttpResponse("ok")