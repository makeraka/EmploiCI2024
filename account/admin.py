from django.contrib import admin
from .models import Etudiant,Teacher
from django.contrib.auth.models import User

# Register your models here.
@admin.register(Etudiant)
class EtudiantAdmin(admin.ModelAdmin):
    list_display = ['user','group']

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    pass


# admin.site.unregister(User)


# Filtre personnalisé
class UserTypeListFilter(admin.SimpleListFilter):
    title = 'Type d\'utilisateur'  # Titre du filtre
    parameter_name = 'user_type'

    def lookups(self, request, model_admin):
        return (
            ('teacher', 'Teacher'),
            ('etudiant', 'Etudiant'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'teacher':
            return queryset.filter(teacher__isnull=False)
        elif self.value() == 'etudiant':
            return queryset.filter(etudiant__isnull=False)
        return queryset

# Désenregistrement du modèle User existant dans l'admin

# Réenregistrement du modèle User avec le filtre personnalisé
# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     list_filter = (UserTypeListFilter,)
#     list_display = ['username','first_name','last_name','etudiant__group']