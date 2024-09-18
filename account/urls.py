from django.urls import path
from . import views
app_name = 'account'
urlpatterns = [
    path('login/', views.loginView, name='app_login'),
    path('register/', views.register, name='app_register'),
    # path('reset/', views.reset, name='app_reset'),
    path('logout/', views.logoutView, name='app_logout'),
]
