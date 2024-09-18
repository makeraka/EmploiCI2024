from django import forms
from django.contrib.auth.models import User
from .models import Etudiant,Teacher
from django.contrib.auth import get_user_model


User = get_user_model()
# Formulaire de traitement de la Classe Etudiant
class EtudiantForm(forms.ModelForm):
    
    class Meta:
        model = Etudiant
        fields = '__all__'
        
        
# Formulaire de traitement du model Teacher
class TeacherForm(forms.ModelForm):
    
    class Meta:
        model = Teacher
        fields = '__all__'

class LoginForm(forms.Form):
    
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control', 
        'placeholder': 'Matricule'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control', 
        'placeholder': 'Mot de passe'
    }))



