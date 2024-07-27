from django.urls import path
from . import views

urlpatterns = [
    path('registrar_chamada/', views.registrar_chamada, name='registrar_chamada'),
    path('registrar_chamada_admin/', views.registrar_chamada_admin, name='registrar_chamada_admin'),
    # outras URLs
]
