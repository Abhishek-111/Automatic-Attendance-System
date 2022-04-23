from django.shortcuts import render
from datetime import datetime as dt
#from xmlrpc.client import DateTime
import cv2 as cv
import numpy as np 
import face_recognition as face_rec
import os
from os import listdir
from os.path import isfile,join
import time
from collections import Counter
from django.contrib import messages 
from ChiefUser import models as m
import smtplib
#for voice
from gtts import gTTS
from playsound import playsound


base_dir = os.getcwd()

def resize(img,size):
    width = int(img.shape[1]*size)
    height = int(img.shape[0]*size)
    dimension = (width,height)
    return cv.resize(img,dimension, interpolation= cv.INTER_AREA)

# path = '/home/abhishek/Gui/Attendance/sample_images' 
path = base_dir+'/core/static/core/sample_images'

employee_img = [] 
employee_name = []
myList = os.listdir(path)
# print(myList)

for cl in myList:
    curImg = cv.imread(f'{path}/{cl}')  # 'sample_img/img_name.jpg'
    employee_img.append(curImg)
    employee_name.append(os.path.splitext(cl)[0]) #splitting img_name from .jpg






# encoding of imgages
def findEncoding(images):
    encoding_list = [] 
    for img in images:
        img = resize(img,0.50)
        img = cv.cvtColor(img,cv.COLOR_BGR2RGB)
        encodeimg = face_rec.face_encodings(img)[0]
        encoding_list.append(encodeimg)
    
    return encoding_list 

encode_list = findEncoding(employee_img)

def dateTime():
    date_t = dt.now()
    return str((date_t.strftime("%d-%m-%Y")))


def sendTheMail(name,mail_id):
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    msg = f"{name}, Your Attendance has been marked for {dateTime()}."
    server.login('ccoding08@gmail.com','JaiShreeRam')

    server.sendmail('ccoding08@gmail.com',f'{mail_id}',msg)
    # print('Mail Sent!!')

def attend_confirmation(name):
    text = f'{name} Your Attendance Has Been Marked!'
    language = 'en'

    voice_obj = gTTS(text=text,lang=language,slow=False)
    print(os.getcwd())
    voice_obj.save(base_dir+f'/core/static/core/att_voices/{name}.mp3')
    playsound(base_dir+f'/core/static/core/att_voices/{name}.mp3')
    # print('sound playing!')
    # Now delete this mp3 file
    os.remove(base_dir+f'/core/static/core/att_voices/{name}.mp3')

global nameList
nameList = []
# Attendance capture  
def Attendance(names):
    # '/home/abhishek/dj/proje/core/static/core/attendance.csv'
    # with open('/home/abhishek/Gui/Attendance/attendance.csv','r+') as f:
    attendance_path = base_dir+'/core/static/core/attendance.csv'
    try:
        with open (f"{base_dir}/core/static/core/attendance_files/{dateTime()}.csv","r+") as f:
        # with open(attendance_path,'r+') as f:
            dataList = f.readlines()
            # nameList = []
            timeList = []
            
        
            for line in dataList:
                # print(line)      ABHI,01/03/2022 (11:01) in next line Name,Time
                entry = line.split(',')
                nameList.append(entry[0])
            
            currTime = dateTime()
            if names not in nameList: #and currTime not in timeList :
                now = dt.now()
                timestr = now.strftime('%d/%m/%y (%H:%M)')
                f.writelines(f'\n{names},{timestr}')
    except FileNotFoundError:
        with open (f"{base_dir}/core/static/core/attendance_files/{dateTime()}.csv","a+") as f:
            pass


            


def step1_verification():
    vid = cv.VideoCapture(0)
    while True:
        success, frame = vid.read()
        smaller_frames = cv.resize(frame,(0,0),None,0.25,0.25) # 0.25 = 1/4th of image
        frames = cv.cvtColor(frame,cv.COLOR_BGR2RGB)

        faces_in_frame = face_rec.face_locations(smaller_frames)
        encodeFacesInFrames = face_rec.face_encodings(smaller_frames,faces_in_frame)

        #compare faces 
        for encodeFace, faceloc in zip(encodeFacesInFrames,faces_in_frame):
            matches = face_rec.compare_faces(encode_list, encodeFace)
            
            #calculating face-distance
            facedist = face_rec.face_distance(encode_list, encodeFace)
            # print(facedist)
            matchIndex = np.argmin(facedist) #minimum face distance

            if matches[matchIndex]:
                # name = employee_name[matchIndex].upper()
                name = employee_name[matchIndex]


                names_lst = []
                names_lst.append(name)

                y1,x2,y2,x1 = faceloc 
                y1,x2,y2,x1 = y1*4,x2*4,y2*4,x1*4 #multiplying each value as it's wrt to smaller frame
                cv.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),3)
                cv.rectangle(frame,(x1, y2-30),(x2,y2),(0,255,0),cv.FILLED)
                cv.putText(frame,name,(x1+6,y2-6),cv.FONT_HERSHEY_COMPLEX,1,(0,0,0),2)
                
                Attendance(name)
        cv.imshow('Live Face Capturing',frame)
        if cv.waitKey(1) == 13:
            break 
    cv.destroyAllWindows()
    return ''.join(names_lst)


# Create your views here.
def startCameraForAttendance(request):
    
    names = step1_verification()

    try:
        person_data = m.EmployeeDetail.objects.get(name = names)
    except:
        pass 

    context = {'status': 'Status','peoples':names.upper()}
    
    sendTheMail(names,person_data.email)
    attend_confirmation(names)
    # print(person_mail)



    return render(request,'TakeAttendance/startCamera.html',context)
