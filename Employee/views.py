from django.shortcuts import render
from django.contrib import messages
from .forms import EmployeeLogin
from ChiefUser import models as m
import os
import pandas as pd

base_dir = os.getcwd()
# Create your views here.

def calAttendance(name):
    totCount = 0
    path = base_dir+'/core/static/core/attendance_files'
    lis = os.listdir(path)
    totDays = 0
    for i in lis:
        dat = pd.read_csv(f'{path}/{i}')
        totCount += dat[dat.Name == name].count()
        totDays+=1

    p = (totCount[0]/totDays)*100
    # return (":.2f".format(p)) 
    return round(p,2)



def emp_login(request):
    sb_sahi = False
    if request.method == 'POST':
        f_obj = EmployeeLogin(request.POST)
        if f_obj.is_valid():
            idName = f_obj.cleaned_data['user_id']
            in_passwd = f_obj.cleaned_data['password']

            try:
                emp_data = m.EmployeeDetail.objects.get(employee_id = idName)
                name = emp_data.name
                real_passwd = emp_data.password
                # print(name)
                percntAtt = calAttendance(name)
                if percntAtt < 50:
                    messages.error(request,f'{name} Your Attendance is {percntAtt}%')
                else:
                    messages.success(request,f'{name} Your Attendance is {percntAtt}%')

                if in_passwd != real_passwd:
                    messages.error(request,"Invalid Credentials! ")
                else:
                    sb_sahi = True
            except:
                messages.error(request,'Please Recheck your Userid! ')
                # print('Not exist!! ')
            # print(id)
            # for emp in emp_data: 
            # print(type(emp_data))
            #     print(emp.name)
            #     print(emp.password)
            
    else:
        f_obj = EmployeeLogin() #blank form
    
    return render(request,'Employee/empLogin.html',{'title':'Employee Login','form':f_obj})
