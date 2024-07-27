from django.shortcuts import render
from .models import Aviso

def lista_avisos(request):
    avisos = Aviso.objects.all().order_by('-data_publicacao')
    return render(request, 'aviso.html', {'avisos': avisos})
