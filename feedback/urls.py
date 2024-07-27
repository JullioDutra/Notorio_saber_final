from django.urls import path
from . import views

urlpatterns = [
    path('aulas/', views.ver_aulas, name='ver_aulas'),
    path('aulas/feedback/<int:chamada_id>/', views.fornecer_feedback, name='fornecer_feedback'),
    path('alunos/presentes/', views.listar_alunos_presentes, name='listar_alunos_presentes'),
    path('alunos/presentes/admin/', views.listar_alunos_presentes_admin, name='listar_alunos_presentes_admin'),
    path('alunos/avaliar/<int:chamada_id>/', views.avaliar_aluno, name='avaliar_aluno'),
]
