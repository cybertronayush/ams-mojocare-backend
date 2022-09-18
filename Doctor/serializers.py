from dataclasses import field
import uuid
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from rest_framework.authtoken.models import Token
from Appointment.models import Appointment

class DoclogSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True, required=True)
    email= serializers.CharField( required=True)
    class Meta:
        model=User
        fields = ['email', 'password']
    def validate(self, attrs):
        user=User.objects.filter(email=attrs['email']).first()
        if user==None:
            raise serializers.ValidationError(
            {"Incorrect User"})
        if not user.check_password(attrs['password']):
            raise serializers.ValidationError(
            {"Incorrect Password"})
        return attrs
    




class DocRegSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    class Meta:
        model=User
        fields=[ 'email', 'username', 'password', 'password2','is_staff']


    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
            {"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            is_staff=True,
        )
        user.set_password(validated_data['password'])
        user.save()
        token=Token.objects.get_or_create(user=user)
        return user


    
class appointSerializer(serializers.ModelSerializer):
    class Meta:
        model=Appointment
        fields='__all__'

    
    