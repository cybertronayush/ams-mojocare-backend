from email.headerregistry import Address
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
import uuid
from Patients.models import Patient


class Appointment(models.Model):
    uid=models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    issue=models.CharField(max_length=600)
    date=models.DateField()
    time=models.TimeField()
    address=models.CharField(max_length=200)
    phonereg=RegexValidator('^(\+91[\-\s]?)?[0]?(91)?[789]\d{9}$')
    number=models.CharField(validators=[phonereg], max_length=13, blank=False)
    doctor=models.EmailField(max_length=100)
    patient=models.EmailField(max_length=100)
    name=models.CharField(max_length=60)
