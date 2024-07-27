from django.urls import path
from . import views

urlpatterns = [
    
    path('professor/', views.pagina_inicial_professor, name='dashboard_professsor'),
    path('administrador/', views.pagina_inicial_admin, name='dashboard_admin'),
    path('aluno/', views.pagina_inicial_aluno, name='dashboard_aluno'),
    
]
