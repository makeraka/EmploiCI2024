from django.urls import path
from . import views
app_name = 'account'
urlpatterns = [
    path('login/', views.loginView, name='app_login'),
    path('register/', views.register, name='app_register'),
    # path('reset/', views.reset, name='app_reset'),
    path('logout/', views.logoutView, name='app_logout'),
    path('teacher_profil/', views.teacher_profil, name="teacher_profil"),
    path('profile/', views.profile, name='profile'),
    path('update-profile/', views.update_student_profile, name='update_student_profile'),
    path('profilprof/<str:prof>/',views.prof_profile_consulting,name="profil_prof")
    
]

