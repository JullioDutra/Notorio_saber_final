from django.urls import path
from . import views

urlpatterns = [
    # outras URLs
    path('relatorio_aluno/', views.relatorio_aluno, name='relatorio_aluno'),
    path('relatorio_arrecadacao_mensal/', views.relatorio_arrecadacao_mensal, name='relatorio_arrecadacao_mensal'),
    path('relatorio_pagamentos_pendentes/', views.relatorio_pagamentos_pendentes, name='relatorio_pagamentos_pendentes'),
    path('relatorio_pagamentos_realizados/', views.relatorio_pagamentos_realizados, name='relatorio_pagamentos_realizados'),
    path('relatorio_boletos_por_mes/', views.relatorio_boletos_por_mes, name='relatorio_boletos_por_mes'),
    path('relatorio_planos_verificados/', views.relatorio_planos_verificados, name='relatorio_planos_verificados'),
    path('relatorios_eventos/', views.relatorios_eventos, name='relatorios_eventos'),
    path('relatorio/feedback/', views.relatorio_feedback, name='relatorio_feedback'),
    path('relatorio/avulsas', views.relatorio_aulas_avulsas, name='relatorio_aulas_avulsas'),
    path('relatorio_desempenho/', views.relatorio_leitura, name='relatorio_desempenho'),
    path('relatorio_professor/', views.relatorio_aulas_mensais_professor, name='relatorio_aulas_mensais_professor'),
    path('relatorio/aulas-reposicao/', views.relatorio_aulas_reposicao, name='relatorio_aulas_reposicao'),
    path('relatorio/aulas-reposicao/exportar-csv/', views.exportar_aulas_reposicao_csv, name='exportar_aulas_reposicao_csv'),

     

]
