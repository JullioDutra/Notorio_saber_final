# perfil/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('perfil_admin', views.perfil_admin, name='perfil_admin'),
    path('perfil_aluno', views.perfil_aluno, name='perfil_aluno'),
    path('perfil_professor', views.perfil_professor, name='perfil_professor'),
]
