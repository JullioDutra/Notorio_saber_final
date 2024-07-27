
from django.shortcuts import render, redirect
from django.contrib import messages
from rolepermissions.decorators import has_permission_decorator
from django.contrib.auth.decorators import login_required
from .models import Aluno, Professor, Chamada
from django.shortcuts import get_object_or_404
from datetime import date
from django.utils import timezone




@login_required
def registrar_chamada_admin(request):
    professor = Professor.objects.get(user=request.user)
    
    if request.method == "POST":
        data = request.POST.get('data', timezone.now().date())

        # Verificar se a data é válida
        if not data:
            messages.error(request, 'Por favor, selecione uma data válida.')
            return redirect('registrar_chamada_admin')

        # Obter a lista de alunos vinculados ao professor
        alunos = professor.alunos.all()

        for aluno in alunos:
            presente = request.POST.get(f'presente_{aluno.id}') == 'on'
            precisa_reposicao = request.POST.get(f'precisa_reposicao_{aluno.id}') == 'on'
            if presente:
                # Criar registro de chamada
                Chamada.objects.create(
                    aluno=aluno, 
                    data=data, 
                    presente=presente, 
                    professor=professor, 
                    precisa_reposicao=precisa_reposicao
                )

                # Diminuir o número de aulas restantes do aluno
                aluno.aulas_restante -= 1
                aluno.save()

        messages.success(request, 'Chamada registrada com sucesso.')
        return redirect('registrar_chamada_admin')

    else:
        # Obter a lista de alunos vinculados ao professor
        alunos = professor.alunos.all()
        context = {
            'alunos': alunos,
            'data': timezone.now().date(),
        }
        return render(request, 'registrar_chamada_admin.html', context)



@login_required
def registrar_chamada(request):
    professor = Professor.objects.get(user=request.user)
    
    if request.method == "POST":
        data = request.POST.get('data', timezone.now().date())

        # Verificar se a data é válida
        if not data:
            messages.error(request, 'Por favor, selecione uma data válida.')
            return redirect('registrar_chamada')

        # Obter a lista de alunos vinculados ao professor
        alunos = professor.alunos.all()

        for aluno in alunos:
            presente = request.POST.get(f'presente_{aluno.id}') == 'on'
            precisa_reposicao = request.POST.get(f'precisa_reposicao_{aluno.id}') == 'on'
            if presente:
                # Criar registro de chamada
                Chamada.objects.create(
                    aluno=aluno, 
                    data=data, 
                    presente=presente, 
                    professor=professor, 
                    precisa_reposicao=precisa_reposicao
                )

                # Diminuir o número de aulas restantes do aluno
                aluno.aulas_restante -= 1
                aluno.save()

        messages.success(request, 'Chamada registrada com sucesso.')
        return redirect('registrar_chamada')

    else:
        # Obter a lista de alunos vinculados ao professor
        alunos = professor.alunos.all()
        context = {
            'alunos': alunos,
            'data': timezone.now().date(),
        }
        return render(request, 'registrar_chamada.html', context)