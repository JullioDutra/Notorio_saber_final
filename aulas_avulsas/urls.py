# aulas_avulsas/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('registrar/', views.registrar_aula_avulsa, name='registrar_aula_avulsa'),
    path('listar/', views.listar_aulas_avulsas, name='listar_aulas_avulsas'),
    path('registrar/admin/', views.registrar_aula_avulsa_admin, name='registrar_aula_avulsa_admin'),
    path('listar/admin/', views.listar_aulas_avulsas_admin, name='listar_aulas_avulsas_admin'),
]
