from django.urls import path
from . import views 

urlpatterns = [
    path('avisos/', views.lista_avisos, name='lista_avisos'),
]
