from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from account.views import signin
# Create your views here.
login_required(login_url=signin)
def home(request):
    
    return render(request,'home.html')


def auth(request):
    return render(request,"auth/auth.html" )

def auth2(request):
    return render(request,"auth/register.html")