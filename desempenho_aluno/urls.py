from django.urls import path
from . import views

urlpatterns = [
    path('configurar/', views.configurar_desempenho, name='configurar_desempenho'),
    path('adicionar-nota/', views.adicionar_nota, name='adicionar_nota'),
    path('desempenho/', views.ver_desempenho, name='ver_desempenho'),
]
