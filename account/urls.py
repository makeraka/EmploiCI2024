from django.urls import path
from account.views import signin,register
urlpatterns = [
    path('signin/',signin, name="connexion"),
    path('register/',register, name="inscription"),
]

