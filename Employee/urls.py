from django.urls import path
from . import views

urlpatterns = [ 
    path('login/',views.emp_login,name = "emplogin")
]
