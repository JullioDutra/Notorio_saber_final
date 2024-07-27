
from django.urls import path
from . import views

urlpatterns = [

    path('cadastrar_aluno/', views.cadastrar_aluno, name='cadastrar_aluno'),
    path('cadastrar_professor/', views.cadastrar_professor, name='cadastrar_professor'),
    path('', views.login, name="login"),
     path('sair/', views.logout, name='sair'),
    path('excluir_usuario/<str:id>/', views.excluir_usuario, name="excluir_usuario"),
    path('usuarios/', views.listar_usuarios, name='listar_usuarios'),
    path('aluno/inativar/<int:aluno_id>/', views.inativar_aluno, name='inativar_aluno'),
    path('aluno/ativar/<int:aluno_id>/', views.ativar_aluno, name='ativar_aluno'),
    path('professor/inativar/<int:professor_id>/', views.inativar_professor, name='inativar_professor'),
    path('professor/ativar/<int:professor_id>/', views.ativar_professor, name='ativar_professor'),
]
    



