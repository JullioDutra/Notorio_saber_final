from django.urls import path
from . import views

urlpatterns = [
    path('contratos_alunos/', views.contratos, name='contratos' )
]
