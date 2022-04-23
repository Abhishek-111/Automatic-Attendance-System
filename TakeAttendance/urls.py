from django.urls import path
from . import views
urlpatterns = [ 
    path('in/',views.startCameraForAttendance, name = 'take_attend')
]