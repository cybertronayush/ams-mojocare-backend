
from sre_constants import SUCCESS
from types import prepare_class
from urllib import response
from urllib.request import Request
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from Doctor.serializers import appointSerializer
from Appointment.models import Appointment
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.authtoken.models import Token
from datetime import time


@api_view(['GET'])
def getappoitment(request, pk):
    data = pk[1:-1]
    try:
        appointment = Appointment.objects.values().get(uid=data)
        serializer = appointSerializer(data=appointment)
        if serializer.is_valid():
            return Response({
                'data': serializer.data
            })
        else:
            return Response({
                'error': serializer.errors
            })
    except Exception as e:
        return Response({
            'Error': 'Cannot find appointment'
        })


@api_view(['PATCH'])
def updateappointment(request, pk):
    data = request.data
    id = pk[1:-1]
    appointment = Appointment.objects.get(pk=id)
    if "issue" in data:
        appointment.issue = data['issue']
    if "name" in data:
        appointment.name = data['name']
    if 'doctor' in data:
        appointment.doctor = data['doctor']
    if 'number' in data:
        appointment.number = data['number']
    if "time" in data:
        appointment.time = data['time']
    appointment.save()
    return Response({
        'status': 'success'
    })


@api_view(['DELETE'])
def deleteappointment(request, pk):
    data = pk[1:-1]
    apointment = Appointment.objects.get(pk=data)
    apointment.delete()
    return Response({
        'status': 'success'
    })
