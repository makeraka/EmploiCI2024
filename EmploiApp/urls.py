from django.urls import path
from . import views

app_name = 'emploi'

urlpatterns = [
    path('',views.home, name="app_home"),
    path('admin/get_prof_dispo/', views.get_prof_dispo, name="get_prof_dispo"),
    path('dispo_salle',views.dispo_salle, name="disp_salle"),
    path('disp',views.dispo, name="dispo"),
    path('editDispo/',views.editDispo, name="app_editDispo"),
    path('delete_dispo/', views.delete_dispo, name='app_delete_dispo'),
]
