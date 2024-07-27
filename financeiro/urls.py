from django.urls import path
from . import views

urlpatterns = [
    # outras URLs
    path('anexar_boleto/', views.anexar_boleto, name='anexar_boleto'),
    path('minha_financa/', views.minha_financa, name='minha_financa'),
    path('validar_comprovante/', views.validar_comprovante, name='validar_comprovante'),
]
