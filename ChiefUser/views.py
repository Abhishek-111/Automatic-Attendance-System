from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import NewRegistration,ChiefUserLogin
from .models import ChiefuserDetail,EmployeeDetail   # for fetching admin details 
from django.contrib import messages
import face_recognition as face_rec
import cv2 as cv 
import os 
import numpy as np
import re
import pandas as pd

# from django.core import validators
# from django import forms

# Create your views here.

base_dir = os.getcwd()

def admin_panel(request):
    if request.user.is_authenticated:
        return render(request, 'ChiefUser/admin_panel.html', {'title': "Admin Panel"})
    else: #authentiacted nhi hai to login kr ke aao
        return HttpResponseRedirect('/chief/admin_login/')  


# name of employee as global ..
nm = 'N'
def addANewEmp(request):
    # form_obj = NewRegistration()
    if request.user.is_authenticated:
        is_error = False
        if request.method == 'POST':
            form_obj = NewRegistration(request.POST)  # obj of class NewRegistration
            if form_obj.is_valid():
                global nm
                nm = form_obj.cleaned_data['name']
                em = form_obj.cleaned_data['email']
                ph = form_obj.cleaned_data['phone_no']
                pss = form_obj.cleaned_data['password']
                cpss = form_obj.cleaned_data['confirm_password']
                address = form_obj.cleaned_data['address']
                 
                # Name Validation 
                if nm.replace(" ", "").isalpha():
                    pass
                else:
                    is_error = True
                    messages.error(request,"Have You forgotten the Name Huh? It's Invalid!")
                    
                # Email Validation 
                if '@' in em:
                    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
                    if(re.fullmatch(regex, em)):
                        pass
                    else:
                        is_error = True
                        messages.error(request,'Invalid Email!')
                else:
                    is_error = True
                    messages.error(request,'Invalid Email!')

                #Phone no validation
                if len(ph) > 10 or len(ph) < 10:
                    is_error = True
                    messages.error(request,'Invalid Phone Number!')
                else:
                    if ph.isdigit() == False:
                        is_error = True
                        messages.error(request,'Invalid Phone Number!')

                # password verification
                if len(pss) >= 6 and len(cpss) >= 6:
                    if pss != cpss:
                        is_error = True
                        messages.error(request,'Password is not Matching!')
                else:
                    is_error = True
                    messages.error(request,'Password should Be atleast 6 chars long!')

                # Address Validation 
                if len(address) < 3:
                    is_error = True
                    messages.error(request,'Invalid Address!')
                else:
                    unwanted = ['@','#','$','%','^','*','!']
                    for i in unwanted:
                        if i in address:
                            is_error = True
                            messages.error(request,'Invalid Address!')

                # If there is no error then save to database.
                if is_error == False:
                    form_obj.save()
                    print('successfully saved to the database.')


                # New Employee form validations Here....
                if len(nm) > 2 and not is_error:
                    return render(request,'ChiefUser/faceSample.html',{'title':'faceSample'})
                    # raise forms.ValidationError('Name should be greater than 2 Chars')
                
        else:
            form_obj = NewRegistration()
    else:
        return HttpResponseRedirect('/chief/admin_login/')
    return render(request,'ChiefUser/addNew.html',{'title': 'New employee Attachment','form':form_obj})


from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate,login,logout

def admin_login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            fm = AuthenticationForm(request = request, data = request.POST)
            if fm.is_valid():
                uname = fm.cleaned_data['username']
                upass = fm.cleaned_data['password']
                user = authenticate(username = uname, password = upass)
                # print('Authenticate Status:',user)
                if user is not None:
                    login(request,user)
                    return HttpResponseRedirect('/chief/admin_panel/')
        else:
            fm = AuthenticationForm()
    else:
        return HttpResponseRedirect('/chief/admin_panel/')
    
    fm = AuthenticationForm()
    return render(request,'ChiefUser/adminLogin.html',{'title':'Admin Login','form':fm})

#LOGOUT 
def user_logout(request):
    logout(request)
    print('logout Successfully!!')
    return HttpResponseRedirect('/chief/admin_login/')



def faceSamplePage(request):
    return render(request,'ChiefUser/faceSample.html',{'title':'Collecting Face Samples'})

def resize(img,size):
    width = int(img.shape[1]*size)
    height = int(img.shape[0]*size)
    dimension = (width,height)
    return cv.resize(img,dimension, interpolation= cv.INTER_AREA)

def takeFaceSample(request):
    # print('The camera will start taking your picture.')

    import cv2 

    key = cv2. waitKey(1)
    webcam = cv2.VideoCapture(0)
    while True:
        try:
            check, frame = webcam.read()
            # print(check) #prints true as long as the webcam is running
            # print(frame) #prints matrix values of each framecd 
            cv2.imshow("Capturing", frame)
            key = cv2.waitKey(1)
            
            smaller_frames = cv2.resize(frame,(0,0),None,0.25,0.25)
            isTherefaces = face_rec.face_locations(smaller_frames)
            
            # if key == ord('s'):
            if isTherefaces:
                fileName_path = f"{base_dir}/core/static/core/sample_images/{nm}.jpg" 
                # fileName_path = f"/home/abhishek/dj/proje/core/static/core/sample_images/{nm}.jpg" 
                # cv2.imwrite(filename=f'{nm}.jpg', img=frame)
                cv2.imwrite(fileName_path, img=frame)
                # print(os.getcwd()) 
                # print(nm)
                webcam.release()
                # img_new = cv2.imread(f'{nm}.jpg', cv2.IMREAD_GRAYSCALE)
                # img_new = cv2.imshow("Captured Image", img_new)
                cv2.waitKey(1650)
                cv2.destroyAllWindows()
            
                print("Image saved!")
            
                break
            elif key == ord('q'):
                print("Turning off camera.")
                webcam.release()
                print("Camera off.")
                print("Program ended.")
                cv2.destroyAllWindows()
                break
            
        except(KeyboardInterrupt):
            print("Turning off camera.")
            webcam.release()
            print("Camera off.")
            print("Program ended.")
            cv2.destroyAllWindows()
            break

            # After collecting the face sample return back to admin home page
    messages.success(request,'Successfully Saved!!')
    return render(request,'ChiefUser/admin_panel.html',{'title':'after collecting face sample'})


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


def check_employees_attendance(request):
    if request.user.is_authenticated:
        empData = EmployeeDetail.objects.all()
        
        # print(data)
    else:
        return HttpResponseRedirect('/chief/admin_login/')
    return render(request,'ChiefUser/empAttendance.html',{'title':'Employees Attendance','empData':empData})

def employees_Info(request,id):
    # id is actually name of employee
    empData = EmployeeDetail.objects.all()
    percnt_att = calAttendance(id)
    if percnt_att < 50:
        messages.error(request,f"{id}'s Attendance is {percnt_att}%")
    else:
        messages.success(request,f"{id}'s Attendance is {percnt_att}%")
    return render(request,'ChiefUser/empAttendance.html',{'title':'Employees Attendance','empData':empData})


