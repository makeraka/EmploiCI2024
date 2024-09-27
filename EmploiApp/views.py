from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from account.models import Etudiant, Teacher
from .models import Course, Seance, ProfDispoWeek
from datetime import datetime, timedelta

@login_required(login_url='account:app_login')
def home(request):

    context = {}
    # Récupérer la date actuelle
    current_date = datetime.now().date()
    current_day_of_week = current_date.weekday()  # 0 = Lundi, 6 = Dimanche

    # Calcul des dates des 7 jours de la semaine
    start_of_week = current_date - timedelta(days=current_day_of_week)
    days_of_week = [start_of_week + timedelta(days=i) for i in range(7)]

    # Récupérer la date sélectionnée
    selected_date_str = request.GET.get('date', current_date)

    # Si la date est une chaîne de caractères, la convertir en date
    if isinstance(selected_date_str, str):
        selected_date = datetime.strptime(selected_date_str, '%Y-%m-%d').date()
    else:
        selected_date = selected_date_str

    # Déterminer le jour de la semaine pour la date sélectionnée
    selected_day_of_week = selected_date.weekday()

    # Vérifier si l'utilisateur est un étudiant
    if Etudiant.objects.filter(user=request.user).exists():
        # Récupérer l'étudiant et son groupe
        student = Etudiant.objects.get(user=request.user)
        student_group = student.group

        # Récupérer les séances pour le groupe de l'étudiant et le jour sélectionné
        seances = Seance.objects.filter(
            group=student_group,
            profDispoWeek__hourRange__day_week=selected_day_of_week
        )
        context['seances'] = seances

    elif Teacher.objects.filter(user=request.user).exists():
        # Récupérer le professeur connecté
        teacher = Teacher.objects.get(user=request.user)

        # Récupérer les séances du professeur pour le jour sélectionné
        seances_teacher = Seance.objects.filter(
            profDispoWeek__teacher=teacher,
            profDispoWeek__hourRange__day_week=selected_day_of_week
        )
        context['seances_teacher'] = seances_teacher

    context['days_of_week'] = days_of_week
    context['selected_date'] = selected_date

    return render(request, 'home.html', context)



def get_prof_dispo(request):
    course_id = request.GET.get('course_id')
    data = []  # Initialiser une liste vide pour les données

    try:
        course = Course.objects.get(id=course_id)
        # Récupérer les disponibilités du professeur pour le cours
        prof_dispos = ProfDispoWeek.objects.filter(teacher=course.Teacher)

        # Construire les données avec les informations de disponibilité
        data = [{
            'id': dispo.id,
            'text': f"{dispo.get_day_week_display()} de {dispo.start_time} à {dispo.end_time}"
        } for dispo in prof_dispos]

    except Course.DoesNotExist:
        # Si le cours n'existe pas, data reste vide
        pass

    return JsonResponse(data, safe=False)

