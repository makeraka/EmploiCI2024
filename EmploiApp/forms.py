from django import forms
from .models import Seance, ProfDispoWeek, Course

class SeanceForm(forms.ModelForm):
    class Meta:
        model = Seance
        fields = '__all__'

    def clean_profDispoWeek(self):
        profDispoWeek = self.cleaned_data.get('profDispoWeek')
        if not profDispoWeek:
            raise forms.ValidationError("Le champ 'Disponibilité du prof' est requis.")
        return profDispoWeek
    



class Dispoform(forms.ModelForm):
        class Meta:
            model = ProfDispoWeek
            fields = ['day_week', 'start_time', 'end_time']  # Assurez-vous d'inclure tous les champs nécessaires
            widgets = {
                'day_week': forms.Select(attrs={
                    'class': 'form-control',
                    'placeholder': 'Sélectionnez le jour de la semaine'  # Optionnel
                }),
                'start_time': forms.TimeInput(attrs={
                    'class': 'form-control',
                    'type': 'time',  # Cela affichera un sélecteur d'heure dans certains navigateurs
                    'placeholder': 'Heure de début'  # Optionnel
                }),
                'end_time': forms.TimeInput(attrs={
                    'class': 'form-control',
                    'type': 'time',  # Cela affichera un sélecteur d'heure dans certains navigateurs
                    'placeholder': 'Heure de fin'  # Optionnel
                }),
             
            }
            labels = {
            'day_week': 'Jour de la semaine',
            'start_time': 'Heure de début',
            'end_time': 'Heure de fin',
            
            }
        
        def clean(self):
            cleaned_data = super().clean()
            start_time = cleaned_data.get('start_time')
            end_time = cleaned_data.get('end_time')

            if start_time and end_time and start_time >= end_time:
                raise forms.ValidationError("L'heure de début doit être inférieure à l'heure de fin.")

            
            return cleaned_data
        


    