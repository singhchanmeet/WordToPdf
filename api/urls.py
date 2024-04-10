from django.urls import path
from . import views

urlpatterns = [    
    path('convert/', views.convert_docx_to_pdf, name='convert_docx_to_pdf'),
]