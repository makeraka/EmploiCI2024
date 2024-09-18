from django.db import models

# Create your models here.


class Department(models.Model):
    
    label = models.CharField(max_length = 150, unique=True)
    deleted = models.BooleanField(default=False)  # Using to control the deleting objects (true= Deleted, False = no deleted), to avoid real deleting in database
    slug = models.SlugField(max_length = 150, unique=True)
    
    def __str__(self):
        return self.label


class Group(models.Model):
    number = models.IntegerField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.number}-{self.department.label}'


class Semestre(models.Model):
    number = models.IntegerField()
    deleted = models.BooleanField(default=False)
    def __str__(self):
        return f'{self.number}'
    




      
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


class Seance(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now=False, auto_now_add=False)
    end_time = models.DateTimeField(auto_now=False, auto_now_add=False)


class HourRange(models.Model):
    start_time = models.DateTimeField(auto_now=False, auto_now_add=False)
    end_time = models.DateTimeField(auto_now=False, auto_now_add=False)
    
    def __str__(self):
        return f'{self.start_time}-{self.end_time}'
    

class ProfDispoWeek(models.Model):
    teacher = models.ForeignKey('account.Teacher', on_delete=models.CASCADE)
    day_week = models.DateField(auto_now=False, auto_now_add=False)
    hourRange = models.ForeignKey(HourRange, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.teacher} - {self.day_week}'
    
    
