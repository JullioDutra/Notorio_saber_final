from django.urls import path
from . import views

urlpatterns = [
    # outras URLs
    path('criar_plano_aula/', views.criar_plano_aula, name='criar_plano_aula'),
    path('listar_planos_aula/', views.listar_planos_aula, name='listar_planos_aula'),
    path('listar_planos_aula_admin/', views.listar_planos_aula_admin, name='listar_planos_aula_admin'),
    path('verificar_plano_aula/<int:plano_id>/', views.verificar_plano_aula, name='verificar_plano_aula'),
]
