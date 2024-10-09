import random
from django.utils.text import slugify
from datetime import timedelta, time, datetime
from EmploiApp.models import Department, Licence, Semestre, Group, Course, Classroom, ProfDispoWeek, Seance
from account.models import Teacher, Etudiant


def load():
    # Définir des valeurs de base pour générer des données aléatoires
    departments = ['DL','NTIC']
    licences = [1, 2, 3]
    semestres = [1, 2, 3, 4, 5, 6]
    groupes = [1, 2]
    courses = ["Algorithmique", "UML", "Gestion d'entreprise", "Big Data"]
    classrooms = ["Salle 101", "Salle 102", "Amphi A", "Amphi B", "Laboratoire 1"]

    # Créer des départements
    for dep in departments:
        department = Department.objects.create(label=dep, slug=slugify(dep))
        print(f"Département créé: {department}")

    # Créer des licences pour chaque département
    for department in Department.objects.all():
        for num in licences:
            licence = Licence.objects.create(number=num, department=department)
            print(f"Licence créée: {licence}")

    # Créer des semestres pour chaque licence
    for licence in Licence.objects.all():
        for num in semestres:
            semestre = Semestre.objects.create(number=num, licence=licence)
            print(f"Semestre créé: {semestre}")

    # Créer des groupes pour chaque licence
    for licence in Licence.objects.all():
        for num in groupes:
            group = Group.objects.create(number=num, licence=licence)
            print(f"Groupe créé: {group}")

    # Créer des cours pour chaque semestre
    for semestre in Semestre.objects.all():
        for course in courses:
            course_instance = Course.objects.create(label=course, semestre=semestre)
            print(f"Cours créé: {course_instance}")

    # Créer des salles de classe
    for room in classrooms:
        classroom = Classroom.objects.create(label=room, capacity=random.randint(20, 100), busy=False)
        print(f"Salle de classe créée: {classroom}")

    # Créer des professeurs et des disponibilités
    for i in range(5):
        teacher = Teacher.objects.create(user_id=random.randint(1, 10), telephone="600123456")
        print(f"Professeur créé: {teacher}")

        for day in range(7):
            start_time = time(hour=random.randint(8, 12))
            end_time = time(hour=start_time.hour + random.randint(1, 3))
            dispo = ProfDispoWeek.objects.create(teacher=teacher, day_week=day, start_time=start_time, end_time=end_time)
            print(f"Disponibilité créée: {dispo}")

    # Créer des séances pour des groupes
    for group in Group.objects.all():
        for _ in range(3):
            course = Course.objects.order_by('?').first()  # Prendre un cours aléatoire
            teacher = Teacher.objects.order_by('?').first()  # Prendre un professeur aléatoire
            classroom = Classroom.objects.order_by('?').first()  # Prendre une salle aléatoire
            day = random.randint(0, 6)  # Jour de la semaine
            h_start = time(hour=random.randint(8, 12))  # Heure de début aléatoire
            h_end = time(hour=h_start.hour + random.randint(1, 3))  # Heure de fin aléatoire
            dispo = ProfDispoWeek.objects.filter(teacher=teacher, day_week=day).first()

            seance = Seance.objects.create(
                course=course,
                professeur=teacher,
                day_week=day,
                h_start=h_start,
                h_end=h_end,
                classroom=classroom,
                profDispoWeek=dispo
            )
            seance.group.add(group)  # Ajouter le groupe à la séance
            print(f"Seance créée: {seance}")
