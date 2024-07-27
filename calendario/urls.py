from django.urls import path
from . import views

urlpatterns = [
    path('adicionar_evento/', views.adicionar_evento, name='adicionar_evento'),
    path('listar_eventos_admin/', views.listar_eventos_admin, name='listar_eventos_admin'),
    path('listar_eventos_professor/', views.listar_eventos_professor, name='listar_eventos_professor'),
    path('listar_eventos_aluno/', views.listar_eventos_aluno, name='listar_eventos_aluno'),
    path('api/eventos/', views.api_eventos, name='api_eventos'),
]
