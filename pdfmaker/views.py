from django.shortcuts import render
from EmploiApp import models
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from EmploiApp.models import Licence,Group,Seance


# Create your views here.

def emploi(request):
    context = {}
    return render(request, 'pdfmaker/show.html', context)


def render_pdf_view(request, licence_id, department_id):
    # Récupérer les séances basées sur la licence et le département
    try:
        # Filtrer les licences
        licence = Licence.objects.get(id=licence_id)
        
        # Filtrer les groupes associés à la licence
        groups = Group.objects.filter(licence=licence)

        # Récupérer les séances pour chaque groupe
        seances = Seance.objects.filter(group__in=groups).select_related('course', 'classroom', 'profDispoWeek')

        # Créer un contexte avec les données nécessaires
        context = {
            'licence': licence,
            'department': licence.department,
            'seances': seances,
        }
        
        template_path = 'pdfmaker/pdf_content.html'
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'filename="Emploi_report.pdf"'
        
        # Trouver le modèle et le rendre
        template = get_template(template_path)
        html = template.render(context)

        # Créer un PDF
        pdf = pisa.pisaDocument(html, dest=response, link_callback=None, encoding='utf-8', 
                                options={'page_size': 'A4', 'orientation': 'landscape'})
        
        # Vérifier les erreurs
        if pdf.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        
        return response

    except Licence.DoesNotExist:
        return HttpResponse('Licence not found.', status=404)
