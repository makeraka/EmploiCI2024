from django.shortcuts import redirect, render
from django.contrib.auth import logout,login


# Create your views here.

def signin(request):
    login(request)
    return render(request,"account/signin.html" )

def register(request):
    return render(request,"account/register.html")


def deconnexion(request):
    logout(request)
    from EmploiApp.views import home
    return redirect(home)