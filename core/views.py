from django.shortcuts import render

# Create your views here.
def home(request):
    context = {'status': 'home_page'}
    return render(request,'core/home.html',context)