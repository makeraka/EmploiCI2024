from django.urls import path
from . import views

app_name = 'emploi'

urlpatterns = [
    path('',views.home, name="app_home"),
    path('p/',views.home, name="app_homeprof"),
    path('admin/get_prof_dispo/',views.get_prof_dispo, name="get_prof_dispo"),
    path('dispo',views.dispo, name="dispo"),
    path('editDispo/<str:pk>/',views.editDispo, name="app-editDispo")
]

