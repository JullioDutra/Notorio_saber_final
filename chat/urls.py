from django.urls import path
from . import views

urlpatterns = [
    path('conversa/<int:destinatario_id>/', views.conversa_atual, name='conversa_atual'),
    path('enviar_mensagem/<int:destinatario_id>/', views.enviar_mensagem, name='enviar_mensagem'),
    path('contatos/', views.lista_contatos, name='lista_contatos'),
    path('iniciar_conversa/<int:destinatario_id>/', views.iniciar_conversa, name='iniciar_conversa'),
    path('recuperar-novas-mensagens/', views.recuperar_novas_mensagens, name='recuperar_novas_mensagens'),
    path('recuperar-contagem-nao-visualizadas/', views.recuperar_contagem_nao_visualizadas, name='recuperar_contagem_nao_visualizadas'),
]
