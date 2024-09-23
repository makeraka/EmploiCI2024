from django.contrib import admin

from EmploiApp.forms import SeanceForm
from .models import ( Department,
                    Group, Licence, Semestre,
                    ProfDispoWeek,
                    Course, Classroom,
                    Seance, HourRange,
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
    list_display = ['teacher','hourRange','busy']
    list_filter = ['teacher','hourRange','busy']

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    pass

@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    pass

@admin.register(Seance)
class SeanceAdmin(admin.ModelAdmin):
    form = SeanceForm
    list_display = ['group', 'course', 'classroom', 'profDispoWeek']
    list_filter = ['group', 'course', 'classroom', 'profDispoWeek__hourRange__day_week']
   
    class Media:
        js = ('assets/js/seance_form.js',)
    

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if 'classroom' in form.base_fields:
            form.base_fields['classroom'].queryset = Classroom.objects.filter(busy=False)
        if 'profDispoWeek' in form.base_fields:
            form.base_fields['profDispoWeek'].queryset = ProfDispoWeek.available.all()  # Utiliser le manager personnalisé
        return form



@admin.register(HourRange)
class HourRangeAdmin(admin.ModelAdmin):
    list_filter  = ['day_week','start_time','end_time']
    
@admin.register(Licence)
class LicenceAdmin(admin.ModelAdmin):
   pass
    # list_filter  = ['day_week','start_time','end_time']
    
