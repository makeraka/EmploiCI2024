
from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse

from django.contrib import messages
from EmploiApp import models as E_model
from .import models as A_model
from .forms import LoginForm,TeacherProfilForm

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
            matricule = request.POST['matricule']
            choosed_department = request.POST['departement']
            department = get_object_or_404(E_model.Department, slug=choosed_department)

            try:
                # Vérification de l'existence de l'étudiant
                etudiant = A_model.Etudiant.objects.get(group__licence__department=department, user__username=matricule) 
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

    
        user = authenticate(username=matricule, password=password)
        if user:
            login(request,user)
            return redirect('emploi:app_home')     
        else:
            messages.error(request,'Informations de connexion invalides')
        
    return render(request,"account/login.html")


######################## methode de doconnexion
def logoutView(request):
    logout(request)
    return redirect('account:app_login')




# **************************** le profil des utilisateurs ***********************************
from django.contrib.auth.decorators import login_required

@login_required
def teacher_profil(request):
    teacher = A_model.Teacher.objects.get(user=request.user)

    if request.method == 'POST':
        form = TeacherProfilForm(request.POST, request.FILES, user=request.user, instance=teacher)
        if form.is_valid():
            print('=========Le formulaire est soumis =======')
            form.save()
            print('=========Le formulaire est save =======')
            messages.success(request, "Les modifications ont été enregistrées avec succès.")
            return redirect('account:teacher_profil')
        else:
            print(f'========={form.errors}============')
    else:
        
        form = TeacherProfilForm(user=request.user, instance=teacher)

    return render(request, 'profil/teacher_profil.html', {'teacher': teacher, 'form': form})







#*********************vue pour le profil sutdent*********************

# def profile(request, username):
#     student = get_object_or_404(A_model.Etudiant, user__username=username)
#     return render(request, 'student/profile.html', {'student': student})

def profile(request):
    if not request.user.etudiant:
        return redirect('emploi:home')
    else:
        student = request.user.etudiant
        return render(request,'student/profile.html',{'student':student})
        
        
        
@login_required
def some_view_that_renders_modal(request, username):
    student = get_object_or_404(A_model.Etudiant, user__username=username)
    groups = E_model.Group.objects.all()  # Récupérer tous les groupes

    return render(request, 'ton_template_avec_modal.html', {
        'student': student,
        'groups': groups,  # Passe les groupes au contexte
    })

# def update_student_profile(request, username):
#     student = get_object_or_404(A_model.Etudiant, user__username=username)
    
#     if request.method == "POST":
#         # Met à jour seulement les champs autorisés
#         student.telephone = request.POST.get('tel', student.telephone)
#         student.adresse = request.POST.get('adress', student.adresse)

#         # Pour l'image, assure-toi de gérer le fichier téléchargé
#         if 'imageStudent' in request.FILES:
#             student.photo = request.FILES['imageStudent']
        
#         student.save()
#         # Redirige ou fais autre chose après la mise à jour
#         return render(request, 'student/profile.html', {'student': student})

#     groups = E_model.Group.objects.all()  # Récupérer tous les groupes pour le formulaire
#     # return render(request, 'student/profile.html', {'student': student, 'groups': groups})



# soumah voici la correction de ta vue:
#primo evite de passer les identifiant dans les urls, donc cette vue ne doit avoir aucun parametre
#tout doit passer par le POST
import os
def update_student_profile(request):
    #il faut d'abord tester si c'est un etudiant qui accèdes, (ces infations sont dans le request)
    if not request.user.etudiant:
        return redirect('emploi:home')
    else:
        student = request.user.etudiant
    
      
        if request.method == "POST":
            student.telephone = request.POST.get('tel', student.telephone)
            student.adresse = request.POST.get('adress', student.adresse)
            if 'imageStudent' in request.FILES:
                if student.photo and os.path.isfile(student.photo.path):
                    os.remove(student.photo.path)
                student.photo = request.FILES['imageStudent']
            student.save()
    return redirect('account:profile')


def prof_profile_consulting(request,prof):
    teacher = get_object_or_404(A_model.Teacher,user__username=prof)
    form = TeacherProfilForm(user=request.user, instance=teacher)
    return render(request,'profil/consulte_profile.html',{'teacher':teacher,'form':form})