from django import forms
from .models import EmpLogin
# from matplotlib import widgets

# class EmployeeLogin(forms.Form):
#     id = forms.CharField(error_messages={'required':'Enter Your Id'})
#     password = forms.CharField(widget=forms.PasswordInput,error_messages={'required':'Enter Your Password'},max_length=6)

    # widgets={
    #     'id':forms.CharField(attrs = {'class':'form-control'}),
    #     'password':forms.PasswordInput(attrs = {'class':'form-control'})
    # }
class EmployeeLogin(forms.ModelForm):
    class Meta:
        model = EmpLogin
        fields = ['user_id','password']

        # for applying bootstrap classes
        widgets = {
            'user_id':forms.TextInput(attrs = {'class':'form-control'}),
            'password':forms.PasswordInput(render_value=False ,attrs={'class':'form-control'}),
        } #
