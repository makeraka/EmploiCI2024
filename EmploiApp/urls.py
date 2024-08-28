from django.urls import path
from . import views
urlpatterns = [
    path('home',views.home, name="home"),
    path('',views.auth, name="auth"),
    path('auth2',views.auth2, name="auth2"),
]

