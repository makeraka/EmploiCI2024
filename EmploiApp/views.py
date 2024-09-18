from django.shortcuts import render
from django.contrib.auth.decorators import login_required


from .models import Seance
from datetime import datetime, timedelta

# from account.views import signin
# Create your views here.


@login_required(login_url='account:app_login')
def home(request):
    # Récupérer la date actuelle
 
    current_date = datetime.now().date()
    print(f'currente date: {current_date}')

    # Calculer les dates des 7 jours de la semaine
    start_of_week = current_date - timedelta(days=current_date.weekday())

    days_of_week = [start_of_week + timedelta(days=i) for i in range(7)]

    # Récupérer le paramètre de la date
    
    selected_date = request.GET.get('date', current_date)
    
    # Récupérer les séances pour la date sélectionnée
    seances = Seance.objects.filter(start_time__date=selected_date)

    context = {
        'days_of_week': days_of_week,
        'seances': seances,
        'selected_date': selected_date,
    }
    return render(request,'home.html',context)



