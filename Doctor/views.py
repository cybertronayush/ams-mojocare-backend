from sre_constants import SUCCESS
from types import prepare_class
from urllib import response
from rest_framework.permissions import AllowAny,IsAuthenticated
from django.contrib.auth.models import User
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from datetime import date,datetime
from Appointment.models import Appointment
from .serializers import DoclogSerializer,DocRegSerializer,appointSerializer
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.authtoken.models import Token

class signup(generics.CreateAPIView):
        queryset = User.objects.all()
        permission_classes = (AllowAny,)
        serializer_class = DocRegSerializer

@api_view(['POST'])
def login(request):
    try:
        data1=request.data
        serializer=DoclogSerializer(data=data1)
        if serializer.is_valid():
            user=User.objects.get(email=data1['email'])
            today = date.today()
            token=Token.objects.filter(user=user).first()
            appointsup=Appointment.objects.values("address", "date", "doctor", "issue", "name", "number", "patient", "time", "uid").filter(doctor=data1['email'])
            upcoming={}
            upcoming['data']=list()
            for i in appointsup:
                print(i['uid'])
                appserial=appointSerializer(data=i)
                if appserial.is_valid():
                    upcoming['data'].append(appserial.data)
                    upcoming['data'][-1]['id']=i['uid']

            return Response({
                'login':'success',
                'data' : serializer.data,
                'access_token' : str(token.key),
                'appointment':upcoming,
            })
        return Response({
           'message':serializer.errors,

        })
                
    except Exception as e:
        return Response({
            'message':str(e),
            'exception':'T'
        })

class getPatientAppointments(APIView):
    def post(self, request, format=None):
        data=request.data
        appointments=Appointment.objects.values().filter(doctor=data['doctor']).filter(patient=data['patient'])
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
                'appointment':upcoming,
            })

@api_view(['GET'])
def getDocappoitment(request,pk):
    data=pk[1:-1]
    appointments=Appointment.objects.values().filter(doctor=data)
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