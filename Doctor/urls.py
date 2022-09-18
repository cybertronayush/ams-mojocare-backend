from django.urls import path
from .views import getPatientAppointments, login, signup, getDocappoitment

urlpatterns = [
    path('signup', signup.as_view()),
    path('login', login),
    path('patientappointments', getPatientAppointments.as_view()),
    path('appointments/<str:pk>', getDocappoitment)

]
