from django.db import models
from .custom_manager import ProfDispoWeekManagerActivation  
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from datetime import datetime, timedelta

# Create your models here.
# CLASS_TYPE =['0']

class Department(models.Model):
    
    label = models.CharField(max_length = 150, unique=True)
    deleted = models.BooleanField(default=False)  # Using to control the deleting objects (true= Deleted, False = no deleted), to avoid real deleting in database
    slug = models.SlugField(max_length = 150, unique=True)
    
    def __str__(self):
        return self.label
    
# ================Le model Licence 
class Licence(models.Model):
    """Model definition for Licence."""
    number = models.IntegerField()
    deleted = models.BooleanField(default=False)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    class Meta:
        

        verbose_name = 'Licence'
        verbose_name_plural = 'Licences'

        unique_together =  ['number','department']

    def __str__(self):
   
        return f'Licence {self.number} {self.department.label}'

# ================Le model Semestre
class Semestre(models.Model):
    number = models.IntegerField()
    licence = models.ForeignKey(Licence, on_delete=models.CASCADE)
    deleted = models.BooleanField(default=False)
    
    def __str__(self):
        return f'Semestre - {self.number} Licence {self.licence.number}'
    

class Group(models.Model):
    number = models.IntegerField()
    licence = models.ForeignKey(Licence, on_delete=models.CASCADE, related_name="groups")
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return f'Licence {self.licence.number}/{self.licence.department.label} Group - {self.number}'


    class Meta:
        unique_together = ['number','licence']


      
class Course(models.Model):
    COURSE_TYPE_CHOICES = [
        ('M', 'Magistral'),
        ('TP', 'Travaux Pratiques'),
    ]
  
    label = models.CharField(max_length=50)
    semestre = models.ForeignKey(Semestre, on_delete=models.CASCADE)
    course_type = models.CharField(max_length=2, choices=COURSE_TYPE_CHOICES, default='M')  # Type de cours
    duration = models.PositiveIntegerField(
        default=1,  # Valeur par défaut pour la durée du cours en heures
        help_text="Durée totale du cours en heures"
    )
    syllabus = models.FileField(upload_to='syllabus/', null=True, blank=True) #plan de cours 
    # teacher = models.ForeignKey('account.Teacher', on_delete=models.CASCADE)  (un cours n'appartient pas à un professeur)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.label}-Sem:{self.semestre}'


class Classroom(models.Model):
    CLASSROOM_TYPE_CHOICES = [
        ('A', 'Amphithéâtre'),
        ('TP', 'Salle de TP'),
    ]

    label = models.CharField(max_length=50)
    classroom_type = models.CharField(max_length=2, choices=CLASSROOM_TYPE_CHOICES, default='A', help_text="Type de la salle")  # Type de salle
    capacity = models.IntegerField()
    busy = models.BooleanField()
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.label

    def check_busy(self):
        #vérifie si une seance est actuellement dans cette classe pour mettre le busy à false ou true
        pass


# class HourRange(models.Model):
#     DAYS_OF_WEEK = [
#         (0, 'Lundi'),
#         (1, 'Mardi'),
#         (2, 'Mercredi'),
#         (3, 'Jeudi'),
#         (4, 'Vendredi'),
#         (5, 'Samedi'),
#         (6, 'Dimanche'),
#     ]
#     day_week = models.IntegerField(choices=DAYS_OF_WEEK)
#     start_time = models.TimeField(auto_now=False, auto_now_add=False)
#     end_time = models.TimeField(auto_now=False, auto_now_add=False)
#     def __str__(self):
#         return f'{self.get_day_week_display()} De {self.start_time}-{self.end_time}'
    
#     class Meta:
#         ordering =  ['day_week']
    



class ProfDispoWeek(models.Model):
    DAYS_OF_WEEK = [
        (0, 'Lundi'),
        (1, 'Mardi'),
        (2, 'Mercredi'),
        (3, 'Jeudi'),
        (4, 'Vendredi'),
        (5, 'Samedi'),
        (6, 'Dimanche'),
    ]
    teacher = models.ForeignKey('account.Teacher', on_delete=models.CASCADE)
    day_week = models.IntegerField(choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()
    busy = models.BooleanField(default=False)  # Vérifie si la disponibilité est affectée ou pas
    occupied_intervals = models.JSONField(default=list, blank=True,null=True)  # Stocker les intervalles occupés
    
    #VALIDATIONS DE DONNEES
    def clean(self):
        super().clean()  # Appel du clean() de la classe parente
        # convertir les temps en datetime pour le même jour
        start_datetime = datetime.combine(datetime.today(), self.start_time)
        end_datetime = datetime.combine(datetime.today(), self.end_time)
        difference_en_heures = (end_datetime - start_datetime) / timedelta(hours=1)

        if difference_en_heures < 2:
            raise ValidationError(
                _('La différence entre l\'heure de début et l\'heure de fin doit être d\'au moins 2 heures, actuellement %(difference)s heures.'),
                params={'difference': difference_en_heures})
       
    def update_intervals(self, new_start=None, new_end=None):
        if new_start is not None and new_end is not None:
            # Convertir les objets time en chaînes
            new_interval = [new_start.strftime('%H:%M:%S'), new_end.strftime('%H:%M:%S')]
            self.occupied_intervals.append(new_interval)

        # Déterminer si la disponibilité est totalement occupée
        total_interval = [self.start_time.strftime('%H:%M:%S'), self.end_time.strftime('%H:%M:%S')]
        occupied = sorted(self.occupied_intervals, key=lambda x: x[0])

        # Vérifier si la liste occupied n'est pas vide avant d'accéder à son premier élément
        if not occupied:
            self.busy = False  # Pas d'intervalle occupé
            return

        merged_intervals = [occupied[0]]
        for current in occupied[1:]:
            last = merged_intervals[-1]
            if current[0] <= last[1]:  # Si les intervalles se chevauchent ou se touchent
                last[1] = max(last[1], current[1])
            else:
                merged_intervals.append(current)

        # Mettre à jour les intervalles fusionnés et vérifier si tout est occupé
        self.occupied_intervals = merged_intervals
        if len(merged_intervals) == 1 and merged_intervals[0] == total_interval:
            self.busy = True
        else:
            self.busy = len(self.occupied_intervals) > 0


    def __str__(self):
        day_name = dict(self.DAYS_OF_WEEK).get(self.day_week, "Jour inconnu")
        return f'{self.teacher}-{day_name} {self.start_time} - {self.end_time}'

# ==================================================================

class Seance(models.Model):
    DAYS_OF_WEEK = [
        (0, 'Lundi'),
        (1, 'Mardi'),
        (2, 'Mercredi'),
        (3, 'Jeudi'),
        (4, 'Vendredi'),
        (5, 'Samedi'),
        (6, 'Dimanche'),
    ]
    
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    professeur = models.ForeignKey('account.Teacher',on_delete=models.CASCADE)  # j'ai ajouté ce champ parce que j'ai brisé la relation entre Teacher et course, donc je ne peux plus avoir accès au teacher via cours, et cours est independant du professeur
    day_week = models.IntegerField(choices=DAYS_OF_WEEK)
    h_start = models.TimeField(auto_now=False, auto_now_add=False)
    h_end = models.TimeField(auto_now=False, auto_now_add=False)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name="seance")
    profDispoWeek = models.ForeignKey(ProfDispoWeek, on_delete=models.CASCADE, verbose_name="Disponibilité du prof")
    group = models.ManyToManyField(Group)

    def save(self, *args, **kwargs):
    # Appeler clean() pour vérifier la validité des données
        self.clean()
        
        # Appeler la méthode save de la classe parente pour sauvegarder la séance
        
        super().save(*args,**kwargs)
    
        # Mettre à jour les intervalles dans la disponibilité du professeur
      
        self.profDispoWeek.update_intervals(self.h_start, self.h_end)
        
        # Marquer la disponibilité du professeur comme occupée
        self.profDispoWeek.busy = True
        self.profDispoWeek.save()

    def delete(self, *args, **kwargs):
        # Récupérer la disponibilité du professeur associée
        prof_dispo = self.profDispoWeek
        
        # Supprimer l'intervalle de temps de la liste des intervalles occupés
        if self.h_start and self.h_end:
            interval_to_remove = [self.h_start.strftime('%H:%M:%S'), self.h_end.strftime('%H:%M:%S')]
            if interval_to_remove in prof_dispo.occupied_intervals:
                prof_dispo.occupied_intervals.remove(interval_to_remove)
        
        # Mettre à jour les disponibilités du professeur
        if prof_dispo.occupied_intervals:
            # Vérifier s'il reste des intervalles occupés
            prof_dispo.busy = True
        else:
            # Aucune disponibilité occupée, donc remettre busy à False
            prof_dispo.busy = False
        
        # Sauvegarder les modifications
        prof_dispo.save()

        # Appeler la méthode de suppression de la classe parente
        super().delete(*args, **kwargs)

    # ... (le reste de votre code ici)



    def clean(self):
        # Vérifier si la disponibilité du professeur est fournie
        if not self.profDispoWeek:
            raise ValidationError(_('Le champ "Disponibilité du prof" est requis.'))

        # Vérifier si le jour de la séance correspond au jour de disponibilité du professeur
        if self.day_week != self.profDispoWeek.day_week:
            raise ValidationError(_('Le jour de la séance ne correspond pas à la disponibilité du professeur.'))

        # Vérifier la validité des horaires
        if self.h_start >= self.h_end:
            raise ValidationError(_('Vérifier vos plages horaires'))

        # Vérifier si l'intervalle demandé est bien inclus dans la disponibilité du professeur
        l = [self.h_start, self.h_end]  # Intervalle de la séance
        r = [self.profDispoWeek.start_time, self.profDispoWeek.end_time]  # Intervalle de la disponibilité du professeur

        if not (l[0] >= r[0] and l[1] <= r[1]):
            raise ValidationError(_("Le professeur n'est pas totalement disponible pendant toute la séance, veuillez revoir les plages horaires"))

        # Vérifier les conflits d'intervalle avec les séances existantes pour ce professeur
        conflicts = Seance.objects.filter(
            profDispoWeek=self.profDispoWeek,
            day_week=self.day_week,
        ).exclude(pk=self.pk)  # Exclure la séance actuelle lors de la mise à jour

        for conflict in conflicts:
            # Vérifier si les intervalles se chevauchent
            if not (self.h_end <= conflict.h_start or self.h_start >= conflict.h_end):
                raise ValidationError(_('Ce professeur est déjà occupé à ce moment.'))

        # Vérifier les conflits pour la salle
        conflicts = Seance.objects.filter(
            classroom=self.classroom,
            day_week=self.day_week,
        ).exclude(pk=self.pk)

        for conflict in conflicts:
            if not (self.h_end <= conflict.h_start or self.h_start >= conflict.h_end):
                raise ValidationError(_('Cette salle est déjà réservée à ce moment pour un autre cours.'))

        # Vérifier les conflits pour le groupe
        
        # print("GROUPE CHOISIS ++++++++",self.group.all())
        # print("jours CHOISIS ++++++++",self.day_week)
        # seances = Seance.objects.filter(day_week=self.day_week)
        # for seance in seances:
        #     conflits = [group for group in seance.group.all() if group in self.group.all()]
        #     if len(conflits)>0:
        #         raise ValidationError("L'un des groupes choisi a deja cours pendant ce temps")
               
        # conflicts = Seance.objects.filter(
        #     group__in=self.group.all(),
        #     day_week=self.day_week,
        # ).exclude(pk=self.pk)
        

        # for conflict in conflicts:
        #     if not (self.h_end <= conflict.h_start or self.h_start >= conflict.h_end):
        #         raise ValidationError(_("L'un des groupes selectionné a déjà une seance à ce moment."))

        # Vérifier la capacité de la salle
        # from account.models import Etudiant
        # nb_student_in_choosed_group = Etudiant.objects.filter(group__in=self.group.all()).count()

        # if nb_student_in_choosed_group > self.classroom.capacity:
        #     raise ValidationError(_(f"Cette classe ne peut pas contenir ce groupe d'étudiants. Sa capacité est de {self.classroom.capacity} places, tandis que le groupe compte {nb_student_in_choosed_group} étudiants."))


        
