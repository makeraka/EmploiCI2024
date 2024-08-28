from django.shortcuts import render

# Create your views here.

def home(request):
    
    return render(request,'home.html')


def auth(request):
    return render(request,"auth/auth.html" )

def auth2(request):
    return render(request,"auth/auth2.html")