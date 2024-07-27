from django.urls import path
from . import views


urlpatterns = [
    path('importar/', views.importar_presenca, name='importar_presenca'),
]