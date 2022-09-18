from django.urls import path,re_path
from .views import getappoitment,updateappointment,deleteappointment

urlpatterns = [
    path('/get-appointment/<str:pk>', getappoitment),
    path('/update/<str:pk>',updateappointment),
    path('/delete',deleteappointment)
    
]