
from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse

from django.contrib import messages
from EmploiApp import models as E_model
from .import models as A_model
from .forms import LoginForm
from django.contrib.auth import get_user_model, authenticate,login,logout

User = get_user_model() 
import re

def register(request):
    # check est un booléen qui permet de contrôler quel formulaire afficher
    # parce qu'il y'a deux formulais html à soumettre dans le templates et les deux jouent chacun un role
    check = True
    context = {}
    departements = E_model.Department.objects.all()

    if request.method == "POST": 
        # le Premier formulaire est soumis
        if request.POST.get('first'):
            pv = request.POST['pv_bac']
            choosed_department = request.POST['departement']
            department = get_object_or_404(E_model.Department, slug=choosed_department)

            try:
                # Vérification de l'existence de l'étudiant
                etudiant = A_model.Etudiant.objects.get(group__licence__department=department, pv=pv) 
                check = False
                context['username'] = etudiant.user.username
            except A_model.Etudiant.DoesNotExist:
                # Message d'erreur si l'étudiant n'est pas trouvé
                messages.add_message(request, messages.ERROR, 'Ces informations ne correspondent à aucun étudiant')
        
        # Le deuxième formulaire est soumis
        else:
            check = False  # en cas de non redirection, il faut retourner au formulaire 2
            # Récupération des informations du formulaire
            username = request.POST.get('username')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')

            # Vérification de la longueur du mot de passe
            if len(password1) < 8:
                messages.add_message(request, messages.ERROR, 'Le mot de passe doit contenir au moins 8 caractères.')
            # Vérification de la complexité du mot de passe (au moins une lettre, un chiffre, et un caractère spécial)
            
            elif password1 != password2:
                messages.add_message(request, messages.ERROR, 'Les mots de passe ne correspondent pas.')
                
            else:
                # Modification du mot de passe de l'utilisateur
                try:
                    user = User.objects.get(username=username)
                    user.set_password(password1)
                    user.is_active = True
                    user.save()
                    messages.add_message(request, messages.SUCCESS, 'Mot de passe modifié avec succès. Vous pouvez maintenant vous connecter.')
                    return redirect('account:app_login')
                except User.DoesNotExist:
                    messages.add_message(request, messages.ERROR, "L'utilisateur spécifié est introuvable.")
    
    context['check'] = check
    context['departements'] = departements

    # Rendre le template avec la variable "check" qui contrôle le formulaire affiché
    return render(request, 'account/register.html', context)


################## methode de connexion
def loginView(request):

    if request.method == 'POST':
        # form = LoginForm(request.POST)
        # if form.is_valid():
        #     form_data = form.cleaned_data
        #     print(form_data)

        matricule = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = authenticate(username=matricule, password=password)
            if user:
                print("j'ai capturé l'utilisateur",user)
                login(request,user)
                print("j'ai loger le l'utilisateur")
                return redirect('emploi:app_home')
                #redirection selon le type de user
                # if user.etudiant:
                #     return redirect('emploi:app_home')
                # elif user.teacher:
                #     return redirect('emploi:app_homeprof')  # pas totalement gérée, je dois y revenir pour achever
        except:
            messages.error(request,'Erreur de Connexion')
        
    return render(request,"account/login.html")


######################## methode de doconnexion
def logoutView(request):
    logout(request)
    return redirect('account:app_login')



