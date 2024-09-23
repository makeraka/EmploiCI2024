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
    licence = models.ForeignKey(Licence, on_delete=models.CASCADE)
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
    busy = models.BooleanField()
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.label




class HourRange(models.Model):
    DAYS_OF_WEEK = [
        (0, 'Lundi'),
        (1, 'Mardi'),
        (2, 'Mercredi'),
        (3, 'Jeudi'),
        (4, 'Vendredi'),
        (5, 'Samedi'),
        (6, 'Dimanche'),
    ]
    day_week = models.IntegerField(choices=DAYS_OF_WEEK)
    start_time = models.TimeField(auto_now=False, auto_now_add=False)
    end_time = models.TimeField(auto_now=False, auto_now_add=False)
    def __str__(self):
        return f'{self.get_day_week_display()} De {self.start_time}-{self.end_time}'
    
    class Meta:
        ordering =  ['day_week']
    



class ProfDispoWeek(models.Model):
    teacher = models.ForeignKey('account.Teacher', on_delete=models.CASCADE)
    hourRange = models.ForeignKey(HourRange, on_delete=models.CASCADE)
    busy = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.teacher} - {self.hourRange}'
    
    class Meta:
        ordering = ['hourRange__day_week']

    # Initialiser correctement les managers
    objects = models.Manager()  # Manager par défaut
    available = ProfDispoWeekManagerActivation()  # Manager personnalisé pour les éléments non occupés





class Seance(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    profDispoWeek = models.ForeignKey(ProfDispoWeek, on_delete=models.CASCADE, verbose_name="Disponibilité du prof")

    def clean(self):
        # Vérifier les conflits pour la salle
        if not self.profDispoWeek:
            raise ValidationError(_('Le champ "Disponibilité du prof" est requis.'))
        conflicts = Seance.objects.filter(
            classroom=self.classroom,
            profDispoWeek__hourRange=self.profDispoWeek.hourRange,
            profDispoWeek__busy=False
        )
        if conflicts.exists():
            raise ValidationError(_('Cette salle est déjà réservée à ce moment pour un autre cours.'))

        # Vérifier les conflits pour le groupe
        conflicts = Seance.objects.filter(
            group=self.group,
            profDispoWeek__hourRange=self.profDispoWeek.hourRange,
            profDispoWeek__busy=False
        )
        if conflicts.exists():
            raise ValidationError(_('Ce groupe a déjà une séance à ce moment.'))

        # Vérifier les conflits pour le professeur
        conflicts = Seance.objects.filter(
            profDispoWeek=self.profDispoWeek,
            profDispoWeek__hourRange=self.profDispoWeek.hourRange,
            profDispoWeek__busy=False
        )
        if conflicts.exists():
            raise ValidationError(_('Ce professeur est déjà occupé à ce moment.'))

    def save(self, *args, **kwargs):
        self.clean()  # Appelle la méthode de validation
        super().save(*args, **kwargs)


