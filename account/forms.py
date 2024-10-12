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







# ******************************* formulaire de profil de teacher****************************
from .models import Teacher  # Assurez-vous d'importer le bon modèle

class TeacherProfilForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=30,
        label='Prénom',
        required=True,

        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg form-control-solid mb-3 mb-lg-0',
            'placeholder': 'Prénom',
            # 'disabled': 'disabled'
        })
    )
    
    last_name = forms.CharField(
        max_length=30,
        label='Nom',
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg form-control-solid mb-3 mb-lg-0',
            'placeholder': 'Nom',
            # 'disabled': 'disabled'
        })
    )
    
    telephone = forms.CharField(
        max_length=15,
        label='Téléphone',
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg form-control-solid',
            'placeholder': 'Numéro de téléphone'
        })
    )
    
    photo = forms.ImageField(
        label='Photo',
        required=False,
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control form-control-lg form-control-solid'
        })
    )
    
    adresse = forms.CharField(
        max_length=255,
        label='Adresse',
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg form-control-solid',
            'placeholder': 'Adresse'
        })
    )
    
    cv = forms.FileField(
        label='CV',
        required=False,
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control form-control-lg form-control-solid'
        })
    )

    class Meta:
        model = Teacher
        fields = ['telephone', 'photo', 'adresse', 'cv']  # Exclure 'user'

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(TeacherProfilForm, self).__init__(*args, **kwargs)
        
        if user is not None:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name