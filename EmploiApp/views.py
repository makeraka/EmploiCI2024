from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# from account.views import signin
# Create your views here.


login_required(login_url='account:app_login')
def home(request):
    
    return render(request,'home.html')


