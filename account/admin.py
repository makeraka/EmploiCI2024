from django.contrib import admin
from .models import Etudiant,Teacher
# Register your models here.
@admin.register(Etudiant)
class EtudiantAdmin(admin.ModelAdmin):
    list_display = ['user','group','pv']

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    pass