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

class PatlogSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True, required=True)
    email= serializers.CharField( required=True)
    class Meta:
        model=User
        fields = ['email', 'password']
    def validate(self, attrs):
        user=User.objects.get(email=attrs['email'])
        if user==None:
            raise serializers.ValidationError(
            {"Incorrect User"})
        if not user.check_password(attrs['password']):
            raise serializers.ValidationError(
            {"Incorrect Password"})
        return attrs
    


class PatRegSerializer(serializers.ModelSerializer):
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
            is_staff=False,
        )
        user.set_password(validated_data['password'])
        user.save()
        token=Token.objects.get_or_create(user=user)
        return user
    
class createappointSerializer(serializers.ModelSerializer):
        class Meta:
            model=Appointment
            fields='__all__'
            # exclude=['uid']
        def validate(self, attrs):
            try:
                if User.objects.get(email=attrs['doctor'])==None:
                    raise serializers.ValidationError(
                {"Invalid doctor"})
            except Exception as e:
                raise serializers.ValidationError(
                {"Invalid doctor"})
            return attrs
        def create(self, validated_data):
            appointment=Appointment.objects.create(
                issue=validated_data['issue'],
                address=validated_data['address'],
                number=validated_data['number'],
                doctor=validated_data['doctor'],
                time=validated_data['time'],
                date=validated_data['date'],
                patient=validated_data['patient'],
                name=validated_data['name'],
            )
            appointment.save()
            return appointment

class doctorSerializer(serializers.ModelSerializer):
        class Meta:
            model=User
            fields=['username']
        def validate(self, attrs):
            user=User.objects.get(username=[attrs['username']])
            if user.is_staff==True :
                raise serializers.ValidationError(
                {"this is admin"})
            return attrs
                    
        

    
    