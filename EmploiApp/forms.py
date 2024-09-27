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
    

