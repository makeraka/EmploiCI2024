from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from account.models import Etudiant
from .models import Seance,Course, ProfDispoWeek
from datetime import datetime, timedelta
from django.http import JsonResponse

# Create your views here.

@login_required(login_url='account:app_login')
def home(request):
    # Récupérer la date actuelle
    current_date = datetime.now().date()
    current_day_of_week = current_date.weekday()  # 0 = Lundi, 6 = Dimanche

    # calcule des dates des 7 jours de la semaine
    start_of_week = current_date - timedelta(days=current_day_of_week)
    days_of_week = [start_of_week + timedelta(days=i) for i in range(7)]

    # Récupérer la date sélectionnée
    selected_date_str = request.GET.get('date', current_date)

    # Si la date est une chaîne de caractères, la convertir en date
    #cette conversion c'est pour pouvoir garder le focuce active sur la date selectionnée dans le template (tout ça pour eviter au max le javascrip)
    if isinstance(selected_date_str, str):
        selected_date = datetime.strptime(selected_date_str, '%Y-%m-%d').date()
    else:
        selected_date = selected_date_str

    # Déterminer le jour de la semaine pour la date sélectionnée
    selected_day_of_week = selected_date.weekday()

    # Récupérer le groupe de l'étudiant authentifié
    try:
        student = Etudiant.objects.get(user=request.user)
        student_group = student.group
    except Etudiant.DoesNotExist:
        return render(request, 'error.html', {'message': "Vous devez être un étudiant pour voir cet emploi du temps."})

    # Récupérer les séances pour le jour sélectionné et le groupe de l'étudiant
    seances = Seance.objects.filter(
        group=student_group,
        profDispoWeek__hourRange__day_week=selected_day_of_week
    )

    context = {
        'days_of_week': days_of_week,
        'seances': seances,
        'selected_date': selected_date,
    }
    return render(request, 'home.html', context)





def get_prof_dispo(request):
    course_id = request.GET.get('course_id')
    try:
        course = Course.objects.get(id=course_id)
        prof_dispos = ProfDispoWeek.objects.filter(teacher=course.Teacher)
        data = [{'id': dispo.id, 'text': str(dispo.hourRange)} for dispo in prof_dispos]
    except Course.DoesNotExist:
        data = []

    return JsonResponse(data, safe=False)


