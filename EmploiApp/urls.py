from django.urls import path
from . import views

app_name = 'emploi'
urlpatterns = [
    path('',views.home, name="app_home"),

]

