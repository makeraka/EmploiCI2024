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
    # list_display = ['teacher','day_week''busy', 'h_start', 'h_end']
    # list_filter = ['teacher','day_week''busy', 'h_start', 'h_end']
    pass
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    pass

@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    pass
@admin.register(Seance)
class SeanceAdmin(admin.ModelAdmin):
    form = SeanceForm
    list_display = ['course', 'day_week', 'classroom', 'profDispoWeek']  # Ajout de day_week
    list_filter = ['course', 'classroom', 'profDispoWeek__day_week', 'profDispoWeek__teacher', 'day_week']  # Ajout de day_week
    
    class Media:
        js = ('assets/js/seance_form.js',)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if 'classroom' in form.base_fields:
            form.base_fields['classroom'].queryset = Classroom.objects.filter(busy=False)
        if 'profDispoWeek' in form.base_fields:
            form.base_fields['profDispoWeek'].queryset = ProfDispoWeek.available.all()  # Utiliser le manager personnalisé
        return form

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
    
