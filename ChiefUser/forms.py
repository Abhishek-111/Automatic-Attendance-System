from django import forms 
from .models import ChiefuserDetail, EmployeeDetail
from django.contrib.auth.forms import User
from django.contrib.auth.forms import AuthenticationForm

class NewRegistration(forms.ModelForm):
    
    class Meta:
        model = EmployeeDetail
        fields = ['name','phone_no','email','employee_id','password','confirm_password','address']
        labels = {
            'name':'Employee Name',
            # 'gender':'Your 'gender'
        }
        error_messages = {
            'name':{'required':'Please Enter Your Name!'},
            # 'gender':{'required':'Please Choose Your Gender'},
            'email':{'required':'Please Enter Your Email!'},
            'phone_no':{'required':'Please Enter Your Phone Number!'},
            'employee_id':{'required':'Please Enter Your Employee Id!'},
            'password':{'required':'Please Enter Password!'},
            'confirm_password':{'required':'Please Re-enter Your Password!'},
            'address':{'required':'Please Enter Your Address!'},
            # 'pincode':{'required':'Please Enter Your Pincode!'}
        }

        widgets = {
            'name':forms.TextInput(attrs = {'class':'form-control'}),
            # 'gender':forms.TextInput(attrs = {'class':'form-control'}),
            'password':forms.PasswordInput(attrs={'class':'form-control'}),
            'confirm_password':forms.PasswordInput(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs = {'placeholder':'abc@yahoo.com','class':'form-control'}),
            'phone_no':forms.TextInput(attrs = {'class':'form-control'}),
            'employee_id':forms.TextInput(attrs = {'class':'form-control'}),
            'address':forms.TextInput(attrs = {'class':'form-control'}),
            # 'pincode':forms.TextInput(attrs = {'class':'form-control'}),
            # 'address':forms.Em
        }
         

#Form for Admin login
# class ChiefUserLogin(forms.ModelForm):
#     class Meta:
#         model = ChiefuserDetail
#         fields = ['chiefUserId','password']
#         labels = {
#             'chiefUserId':'Enter Your ID',
#             'password':'Password'
#         }

#         widgets = {
#             'chiefUserId':forms.TextInput(attrs={'class':'form-control'}),
#             'password':forms.PasswordInput(attrs={'class':'form-control'}),
#         }
#         error_messages = {
#             'chiefUserId':{'required':'Please Enter Your User ID'},
#             'password':{'required':'Please Enter Your Password'}
            
#         }


class ChiefUserLogin(AuthenticationForm):
    class Meta:
        model = User #AuthenticationForm
        fields = ['username','password']
        labels = {
            'username':'Enter Your ID',
            'password':'Password'
        }

        widgets = {
            'username':forms.TextInput(attrs={'class':'form-control'}),
            'password':forms.PasswordInput(attrs={'class':'form-control'}),
        }
        error_messages = {
            'username':{'required':'Please Enter Your User ID'},
            'password':{'required':'Please Enter Your Password'}
            
        }



























# applying form Validation 
    # def clean_name(self):
    #     valname = self.cleaned_data['name']
    #     if len(valname) < 2:
    #         raise forms.ValidationError('Invalid Name!')

    # def clean(self):
    #     cleaned_data = super().clean()
    #     val_name = self.cleaned_data['name']
    #     val_gender = self.cleaned_data['gender']
    #     val_phone = self.cleaned_data['phone']
    #     val_email = self.cleaned_data['email']
    #     val_employee_id = self.cleaned_data['employee_id']
    #     val_password = self.cleaned_data['password']
    #     # val_confirm_password = self.cleaned_data['confirm_password']
    #     val_address = self.cleaned_data['address']
    #     val_pincode = self.cleaned_data['pincode']

        # applying validations:--
        # print(val_address)
        # print(val_name)
        # print(val_phone)
        # print(val_password)
        # print(val_pincode)
        # print(val_email)


