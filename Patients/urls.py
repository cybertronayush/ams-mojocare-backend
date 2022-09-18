from django.urls import path
from .views import login, signup, createAppointment, gettimeslots, getPatappoitment

urlpatterns = [
    path('signup', signup.as_view()),
    path('login', login),
    path('createappointment', createAppointment.as_view()),
    path('get-time-slots', gettimeslots),
    path('appointments/<str:pk>', getPatappoitment)

]
