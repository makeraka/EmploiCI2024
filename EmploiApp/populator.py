
import random
from datetime import time
from account.models import Teacher
from EmploiApp.models import *

def pop():
    # Récupérer tous les enseignants
    teachers = Teacher.objects.all()

    # Jours de la semaine (Lundi à Dimanche)
    DAYS_OF_WEEK = list(range(7))

    # Générer des disponibilités pour chaque enseignant
    for teacher in teachers:
        for day in DAYS_OF_WEEK:
            # Nombre aléatoire de disponibilités à créer pour chaque jour (entre 0 et 3)
            num_entries = random.randint(0, 3)
            for _ in range(num_entries):
                # Générer des heures de début et de fin aléatoires (durée de 2 à 3 heures)
                start_hour = random.randint(8, 17)  # Heure de début entre 8h et 17h
                start_minute = random.choice([0, 30])  # Commence soit à l'heure pile, soit à 30 minutes
                end_hour = start_hour + random.choice([2, 3])  # Durée de 2 ou 3 heures

                # S'assurer que l'heure de fin ne dépasse pas 19h (7 PM)
                if end_hour > 19:
                    end_hour = 19

                start_time = time(hour=start_hour, minute=start_minute)
                end_time = time(hour=end_hour, minute=start_minute)

                # Créer une instance de ProfDispoWeek
                ProfDispoWeek.objects.create(
                    teacher=teacher,
                    day_week=day,
                    start_time=start_time,
                    end_time=end_time,
                    busy=False
                )

    print("Les instances de ProfDispoWeek ont été créées avec succès.")

# Exécuter la fonction si le fichier est appelé directement
if __name__ == "__main__":
    populate_prof_dispo()
