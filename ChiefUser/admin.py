from django.contrib import admin
from .models import EmployeeDetail,ChiefuserDetail

# used to save into Database.

@admin.register(EmployeeDetail)
# Register your models here.
class EmployeeDetailAdmin(admin.ModelAdmin):
    list_display = ('id','name','phone_no','email','employee_id','password','address')
    
@admin.register(ChiefuserDetail)
class ChiefuserDetailAdmin(admin.ModelAdmin):
    list_display = ('id','chiefUserId','password')
