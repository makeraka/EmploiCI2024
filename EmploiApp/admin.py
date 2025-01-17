from django.contrib import admin

from EmploiApp.forms import SeanceForm
from .models import ( Department,
                    Group, Licence, Semestre,
                    ProfDispoWeek,
                    Course, Classroom,
                    Seance
                    )

# Register your models here.



@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("label",)}
    
@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    pass


@admin.register(Semestre)
class SemestreAdmin(admin.ModelAdmin):
    pass



@admin.register(ProfDispoWeek)
class ProfDispoWeekAdmin(admin.ModelAdmin):
    list_display = ['teacher','day_week','busy', 'start_time', 'end_time']
    list_filter = ['teacher','day_week']
    pass
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_filter = ['semestre']

@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    pass
@admin.register(Seance)
# class SeanceAdmin(admin.ModelAdmin):
#     form = SeanceForm
#     list_display = ['course','professeur', 'day_week', 'classroom', 'profDispoWeek']  
#     list_filter = ['course','professeur', 'classroom', 'professeur', 'day_week']  
    
#     class Media:
#         js = ('assets/js/charge_dispo.js',)

    

#     def save_model(self, request, obj, form, change):
#         # Enregistrer d'abord l'objet pour obtenir un ID
#         super().save_model(request, obj, form, change)
        
#         # Maintenant que l'objet est sauvegardé, vous pouvez gérer le champ ManyToMany
#         # Vérifiez si des groupes ont été sélectionnés dans le formulaire
#         if form.cleaned_data.get('group'):
#             obj.group.set(form.cleaned_data['group'])


class SeanceAdmin(admin.ModelAdmin):
    form = SeanceForm
    list_display = ['course', 'day_week', 'classroom', 'profDispoWeek']  # Ajout de day_week
    list_filter = ['course', 'classroom', 'profDispoWeek__day_week', 'profDispoWeek__teacher', 'day_week']  # Ajout de day_week
    
    class Media:
        js = ('assets/js/charge_dispo.js',)

    def save_model(self, request, obj, form, change):
        # Enregistrer d'abord l'objet pour obtenir un ID
        super().save_model(request, obj, form, change)
        
        # Maintenant que l'objet est sauvegardé, vous pouvez gérer le champ ManyToMany
        # Vérifiez si des groupes ont été sélectionnés dans le formulaire
        if form.cleaned_data.get('group'):
            obj.group.set(form.cleaned_data['group'])



    
@admin.register(Licence)
class LicenceAdmin(admin.ModelAdmin):
   pass
    # list_filter  = ['day_week','start_time','end_time']
    
