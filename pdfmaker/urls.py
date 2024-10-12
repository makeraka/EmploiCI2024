from django.urls import path
from . import views
urlpatterns = [
    path('emploi/',views.emploi, name="emploi"),
    path('create-pdf',views.render_pdf_view, name='create_pdf')
    #  path('create-pdf/<int:licence_id>/<int:department_id>/', views.render_pdf_view, name='create_pdf'),
]

