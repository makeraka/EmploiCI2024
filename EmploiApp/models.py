from django.db import models
from .custom_manager import ProfDispoWeekManagerActivation  
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


# Create your models here.


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
        return f'{self.number}'
    

class Group(models.Model):
    number = models.IntegerField()
    licence = models.ForeignKey(Licence, on_delete=models.CASCADE, related_name="groups")
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return f'Licence {self.licence.number}/{self.licence.department.label} Group - {self.number}'


    class Meta:
        unique_together = ['number','licence']


      
class Course(models.Model):
  
    label = models.CharField(max_length=50)
    semestre = models.ForeignKey(Semestre, on_delete=models.CASCADE)
    Teacher = models.ForeignKey('account.Teacher', on_delete=models.CASCADE)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.label}-Sem:{self.semestre}'


class Classroom(models.Model):
    label = models.CharField(max_length=50)
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
    start_time = models.TimeField(auto_now=False, auto_now_add=False)
    end_time = models.TimeField(auto_now=False, auto_now_add=False)
    busy = models.BooleanField(default=False) #vérifie si la disponibilité est affecté ou pas

    def __str__(self):
        return f'{self.teacher} - {self.get_day_week_display()} de {self.start_time} à {self.end_time}'
    
    class Meta:
        ordering = ['day_week']
    objects = models.Manager()  # Manager par défaut
    available = ProfDispoWeekManagerActivation()  # Manager personnalisé pour les éléments non occupés

# ===================================================================
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
    group = models.ManyToManyField(Group)
    # group = models.ManyToManyField(Group, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)    
    day_week = models.IntegerField(choices=DAYS_OF_WEEK)
    h_start = models.TimeField(auto_now=False, auto_now_add=False)
    h_end = models.TimeField(auto_now=False, auto_now_add=False)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    profDispoWeek = models.ForeignKey(ProfDispoWeek, on_delete=models.CASCADE, verbose_name="Disponibilité du prof")

def save(self, *args, **kwargs):
    # Étape 1 : Enregistrer l'instance sans assigner les groupes
    if not self.pk:  # Si l'objet n'a pas encore d'ID
        super(Seance, self).save(*args, **kwargs)

    # Étape 2 : Assigner les groupes, maintenant que l'ID est disponible
    if 'groups' in kwargs:
        groups = kwargs.pop('groups')
        self.group.set(groups)

    # Étape 3 : Enregistrer à nouveau l'instance pour s'assurer que tous les changements sont sauvegardés
    super(Seance, self).save(*args, **kwargs)


    def clean(self):
        # Vérifier si la disponibilité du professeur est fournie
        if not self.profDispoWeek:
            raise ValidationError(_('Le champ "Disponibilité du prof" est requis.'))

        # Vérifier si le jour de la séance correspond au jour de disponibilité du professeur
        if self.day_week != self.profDispoWeek.day_week:
            raise ValidationError(_('Le jour de la séance ne correspond pas à la disponibilité du professeur.'))



        if self.h_start >= self.h_end:
            raise ValidationError(_('Vérifier vos plages horaires'))


        """
       [self.h_start,self.h_end]inclu [pdw.start_time,pdw.end_time]
       ??
       si self.h_start >= pdw.start_time et self.h_end <= pdw.end_time


        """
  
        l= [self.h_start,self.h_end] # l: signifie left_interval
        r= [self.profDispoWeek.start_time,self.profDispoWeek.end_time] # r: signifie right_interval

        if not (l[0]>=r[0] and l[1]<=r[1]):
            raise ValidationError(_("le professeur n'est pas totalement disponible pendant toute la seance, veuillez revoir les plages horaires"))

        # Vérifier les conflits pour la salle
        conflicts = Seance.objects.filter(
            classroom=self.classroom,
            day_week=self.day_week,
            # h_start__lt=self.h_end,   # on ne peut pas créer une seance dont l'heure de depart est inférieur à l'une des s"ance qui existe deja
            # h_end__gt=self.h_start,     
            profDispoWeek__busy=False
        )
        if conflicts.exists():
            raise ValidationError(_('Cette salle est déjà réservée à ce moment pour un autre cours.'))

        # Vérifier les conflits pour le groupe
        conflicts = Seance.objects.filter(
            group=self.group,
            day_week=self.day_week,
            # h_start__lt=self.h_end,
            # h_end__gt=self.h_start,
            profDispoWeek__busy=False
        )
        if conflicts.exists():
            raise ValidationError(_('Ce groupe a déjà une séance à ce moment.'))

        # Vérifier les conflits pour le professeur
        conflicts = Seance.objects.filter(
            profDispoWeek=self.profDispoWeek,
            day_week=self.day_week,
            # h_start__lt=self.h_end,
            # h_end__gt=self.h_start,
            profDispoWeek__busy=False
        )
        if conflicts.exists():
            raise ValidationError(_('Ce professeur est déjà occupé à ce moment.'))

        
        # checking de la capacité de la salle  =====================================
        """
        1- recupérer le nombre d'Etudiant dans le groupe choisi
        2- comparer ce nombre à la capacité de la salle
        3- lever une exception  en cas de supériorité au niveau du nombre d'Etudiant
        
        """
        from account.models  import Etudiant
        nb_student_in_choosed_group = Etudiant.objects.filter(group=self.group).count()

        if nb_student_in_choosed_group > self.classroom.capacity:
            raise ValidationError(_(f"Cette classe ne peut pas contenir ce groupe d'Etudiant sa capacité est {self.classroom.capacity} Place\n et le groupe compte {nb_student_in_choosed_group} Etudiants"))

        
    def save(self, *args, **kwargs):
        self.clean()  # Appelle la méthode de validation
        super().save(*args, **kwargs)


