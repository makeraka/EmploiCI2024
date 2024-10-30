from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views,views_prof

urlpatterns = [
    path('emploi/',views.emploi, name="emploi"),
    path('create-pdf',views.render_pdf_view, name='create_pdf'),
    path('create-pdf_prof',views_prof.render_pdf_view_prof, name='create_pdf_prof'),
    
    #  path('create-pdf/<int:licence_id>/<int:department_id>/', views.render_pdf_view, name='create_pdf'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

