# views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Evento, Users
from rolepermissions.decorators import has_permission_decorator

@login_required
def adicionar_evento(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        descricao = request.POST.get('descricao')
        tipo = request.POST.get('tipo')
        data_inicio = request.POST.get('data_inicio')
        data_fim = request.POST.get('data_fim')
        usuarios_destinados = request.POST.getlist('usuarios_destinados')

        evento = Evento.objects.create(
            titulo=titulo,
            descricao=descricao,
            tipo=tipo,
            data_inicio=data_inicio,
            data_fim=data_fim
        )
        evento.usuarios_destinados.set(usuarios_destinados)
        evento.save()
        return redirect('listar_eventos_admin')
    
    usuarios = Users.objects.all()
    return render(request, 'adicionar_evento.html', {'usuarios': usuarios})



@login_required
def listar_eventos(request):
    if request.user.cargo == 'A':
        eventos = Evento.objects.all()
    else:
        eventos = request.user.eventos.all()
    return render(request, 'listar_eventos.html', {'eventos': eventos})



@login_required
def listar_eventos_admin(request):
    if request.user.cargo == 'A':
        eventos = Evento.objects.all()
    else:
        eventos = request.user.eventos.all()
    return render(request, 'listar_eventos_admin.html', {'eventos': eventos})


@login_required
def listar_eventos_professor(request):
    if request.user.cargo == 'A':
        eventos = Evento.objects.all()
    else:
        eventos = request.user.eventos.all()
    return render(request, 'listar_eventos_professor.html', {'eventos': eventos})

@login_required
def listar_eventos_aluno(request):
    if request.user.cargo == 'A':
        eventos = Evento.objects.all()
    else:
        eventos = request.user.eventos.all()
    return render(request, 'listar_eventos_aluno.html', {'eventos': eventos})



def api_eventos(request):
    eventos = Evento.objects.all()
    eventos_data = []

    for evento in eventos:
        eventos_data.append({
            'id': evento.id,
            'title': evento.titulo,
            'start': evento.data_inicio.isoformat(),
            'end': evento.data_fim.isoformat(),
            'description': evento.descricao,
            'type': evento.tipo
        })

    return JsonResponse(eventos_data, safe=False)
