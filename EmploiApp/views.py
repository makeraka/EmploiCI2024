from django.http import JsonResponse
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from account.models import Etudiant, Teacher
from .models import Course, Seance, ProfDispoWeek
from datetime import datetime, timedelta
from django.core.paginator import Paginator
from .forms import Dispoform
from django.contrib import messages
from django.views.generic import UpdateView,DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.db.models import Q
from datetime import datetime, timedelta

@login_required(login_url='account:app_login')
@login_required(login_url='account:app_login')
def home(request):
    context = {}
    # Récupératon de la date actuelle
    current_date = datetime.now().date()
    current_day_of_week = current_date.weekday()  # 0 = Lundi, 6 = Dimanche

    # Calcul des dates des 7 jours de la semaine
    start_of_week = current_date - timedelta(days=current_day_of_week)
    days_of_week = [start_of_week + timedelta(days=i) for i in range(7)]

    # Récupération de la date sélectionnée
    selected_date_str = request.GET.get('date', current_date)

    # Si la date est une chaîne de caractères, la convertir en date
    if isinstance(selected_date_str, str):
        selected_date = datetime.strptime(selected_date_str, '%Y-%m-%d').date()
    else:
        selected_date = selected_date_str

    # Déterminer le jour de la semaine pour la date sélectionnée
    selected_day_of_week = selected_date.weekday()

    # Trouver la séance actuelle (pour pouvoir la signalé comme en cours)
    now = datetime.now().time()  # Heure actuelle
    current_seance = None

    # Vérifier si l'utilisateur est un étudiant
    if Etudiant.objects.filter(user=request.user).exists():
        # Récupérer l'étudiant et son groupe
        student = Etudiant.objects.get(user=request.user)
        student_group = student.group

        # Récupérer les séances pour le groupe de l'étudiant et le jour sélectionné
        seances = Seance.objects.filter(
            group=student_group,
            profDispoWeek__day_week=selected_day_of_week
        )

        # Trouver la séance actuelle
        current_seance = Seance.objects.filter(
            group=student_group,
            profDispoWeek__day_week=selected_day_of_week,
            profDispoWeek__start_time__lte=now,
            profDispoWeek__end_time__gte=now
        ).first()

        context['seances'] = seances

    elif Teacher.objects.filter(user=request.user).exists():
        # Récupérer le professeur connecté
        teacher = Teacher.objects.get(user=request.user)

        # Récupérer les séances du professeur pour le jour sélectionné
        seances_teacher = Seance.objects.filter(
            profDispoWeek__teacher=teacher,
            profDispoWeek__day_week=selected_day_of_week
        )

        # Trouver la séance actuelle
        current_seance = Seance.objects.filter(
            profDispoWeek__teacher=teacher,
            profDispoWeek__day_week=selected_day_of_week,
            profDispoWeek__start_time__lte=now,
            profDispoWeek__end_time__gte=now
        ).first()

        context['seances_teacher'] = seances_teacher

    context['days_of_week'] = days_of_week
    context['selected_date'] = selected_date
    context['current_seance'] = current_seance  # Ajoutez ceci au contexte

    return render(request, 'home.html', context)


def get_prof_dispo(request):
    course_id = request.GET.get('course_id')
    data = []  # Initialiser une liste vide pour les données

    try:
        course = Course.objects.get(id=course_id)
        # Récupérer les disponibilités du professeur pour le cours
        prof_dispos = ProfDispoWeek.objects.filter(teacher=course.teacher)

        # Construire les données avec les informations de disponibilité
        data = [{
            'id': dispo.id,
            'text': f"{dispo.get_day_week_display()} de {dispo.start_time} à {dispo.end_time}"
        } for dispo in prof_dispos]

    except Course.DoesNotExist:
        # Si le cours n'existe pas, data reste vide
        pass

    return JsonResponse(data, safe=False)





#*********************vue pour la disponibilité des professeurs *********************
@login_required(login_url="account:app_login")
def dispo(request):
    user = request.user
    try:
        owner = Teacher.objects.get(user=user)
    except Teacher.DoesNotExist:
        return redirect('account:app_logout')

    if request.method == "POST":
        form = Dispoform(request.POST)
        if form.is_valid():
            dispo = form.save(commit=False)
            dispo.teacher = owner
            dispo.save()  # Sauvegarde de la disponibilité

            # Mettre à jour les intervalles de disponibilité
            dispo.update_intervals(dispo.start_time, dispo.end_time)

            messages.success(request, "Disponibilité ajoutée avec succès")

        else:
            messages.error(request, 'Vous avez commis une erreur dans la saisie, veuillez réessayer')
            for field in form:
                for error in field.errors:
                    messages.error(request, error)
    search_day = request.GET.get('search_day')
    dispo_list = ProfDispoWeek.objects.filter(teacher=owner).order_by('day_week', 'start_time')

    if search_day is not None and search_day != '':
        dispo_list = dispo_list.filter(day_week=int(search_day))

    # Pagination
    paginator = Paginator(dispo_list, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    for dispo in page_obj:
        print("Occupied intervals:", dispo.occupied_intervals)  # Ajoutez ceci avant de retourner le contexte

    context = {
        "dispos": page_obj,
        'form': Dispoform(),
    }

    return render(request, "teacher/dispo.html", context)

@login_required(login_url="account:app_login")
def editDispo(request):
    if request.method == "POST":
        dispo_id = request.POST.get('dispo_id')
        day_week = request.POST.get('day_week')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')

        # Vérifiez si dispo_id est fourni et est un entier
        if dispo_id:
            try:
                dispo_id = int(dispo_id)
                # Essayez de récupérer l'instance existante
                instance = ProfDispoWeek.objects.get(id=dispo_id)
                
                # Mettez à jour les champs de l'instance
                instance.day_week = day_week
                instance.start_time = start_time
                instance.end_time = end_time
                instance.save()

                messages.success(request, 'Disponibilité modifiée avec succès')
            except ProfDispoWeek.DoesNotExist:
                messages.error(request, 'La disponibilité spécifiée n\'existe pas.')
            except ValueError:
                messages.error(request, 'ID de disponibilité invalide.')
            except Exception as e:
                messages.error(request, f'Erreur : {str(e)}')

       

    return redirect('emploi:dispo')  # Redirection en cas de requête GET ou d'erreur


@login_required(login_url="account:app_login")
def delete_dispo(request):
    # Récupérer l'ID de la disponibilité à supprimer depuis la requête POST
    dispo_id = request.POST.get('dispo-id')
    # Vérifier si la disponibilité existe
    dispo = get_object_or_404(ProfDispoWeek, pk=dispo_id)
    #vérification si la disponibilité est déja assigné
    try:
        # Supprimer la disponibilité
        dispo.delete()
        # Ajouter un message de succès
        messages.success(request, 'La disponibilité a été supprimée avec succès.')
    except Exception as e:
        # Ajouter un message d'erreur en cas de problème
        messages.error(request, f'Erreur lors de la suppression de la disponibilité : {str(e)}')

    # Rediriger vers la page de liste des disponibilités
    return redirect('emploi:dispo') 