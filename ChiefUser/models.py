from django.db import models

import ChiefUser

# Create your models here.
class EmployeeDetail(models.Model):
    name = models.CharField(max_length=25)
    # gender = models.Choices([('M','Male'),('F','Female')])
    # gender = models.CharField(max_length=6)
    phone_no = models.CharField(max_length=10)
    email = models.EmailField(max_length=35)
    employee_id = models.CharField(max_length=15)
    password = models.CharField(max_length=10)
    confirm_password=models.CharField(max_length=10)  # not required
    address = models.CharField(max_length=80)
    # pincode = models.CharField(max_length=6)

#It includes the Admin login Id and password 
class ChiefuserDetail(models.Model):
    chiefUserId = models.CharField(max_length=25)
    password = models.CharField(max_length=10)