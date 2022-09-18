from sre_constants import SUCCESS
from types import prepare_class
from urllib import response
from rest_framework.permissions import AllowAny,IsAuthenticated
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from Doctor.serializers import appointSerializer
from Appointment.models import Appointment
from .serializers import PatlogSerializer,PatRegSerializer,createappointSerializer
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.authtoken.models import Token
from datetime import time

class signup(generics.CreateAPIView):
        queryset = User.objects.all()
        permission_classes = (AllowAny,)
        serializer_class = PatRegSerializer

@api_view(['POST'])
def login(request):
    try:
        data1=request.data
        serializer=PatlogSerializer(data=data1)
        if serializer.is_valid():
            user=User.objects.get(email=data1['email'])
            
            token=Token.objects.get(user=user)
            appointsup=Appointment.objects.values("address", "date", "doctor", "issue", "name", "number", "patient", "time", "uid").filter(patient=data1['email'])
            upcoming={}
            upcoming['data']=list()
            for i in appointsup:
                print(i)
                appserial=appointSerializer(data=i)
                if appserial.is_valid():
                    upcoming['data'].append(appserial.data)
                    upcoming['data'][-1]['id']=i['uid']
            doctordata={}
            doctordata['name']=list()
            doctors=User.objects.only('email').filter(is_staff=True).filter(is_superuser=False)
            print(doctors)
            for i in doctors:
                doctordata['name'].append(str(i))
            
            return Response({
                'login':'success',
                'data' : serializer.data,
                'access_token' : str(token.key),
                'doctors': doctordata,
                'appointments': upcoming,
            })
        return Response({
           'message':serializer.errors,

        })
                
    except Exception as e:
        return Response({
            'message':str(e)
        })

class createAppointment(generics.CreateAPIView):
        permission_classes = (AllowAny,)
        serializer_class = createappointSerializer

@api_view(['POST'])
def gettimeslots(request):
    altimeslots=list()
    starttime=36000
    slotlist={}
    slotlist['data']=list()
    for i in range(16):
        t=starttime+i*1800
        hour = (t)//3600 
        min = (t -  + (hour*3600))//60 
        seconds = t - ( (hour*3600) + (min*60)) 
        print(time(hour,min,seconds))
        altimeslots.append(time(hour,min,seconds))
    try:
        data=request.data
        doctor=data['name']
        date=data['date']
        appointments=Appointment.objects.values('time').filter(doctor=doctor).filter(date=date)
        timeset=set()
        for i in appointments:
            timeset.add(i['time'])
        for i in altimeslots:
            if i not in timeset:
                slotlist['data'].append(i)
        return Response({
        'Timeslots':slotlist
        })
    except Exception as e:
        return Response({
            'errormessage': str(e)
        })

@api_view(['GET'])
def getPatappoitment(request,pk):
    data=pk[1:-1]
    appointments=Appointment.objects.values().filter(patient=data)
    upcoming={}
    upcoming['data']=list()
    for i in appointments:
        print(i['uid'])
        appserial=appointSerializer(data=i)
        if appserial.is_valid():
            upcoming['data'].append(appserial.data)
            upcoming['data'][-1]['id']=i['uid']

    return Response({
            'status':'success',
                'appointment':upcoming,})

