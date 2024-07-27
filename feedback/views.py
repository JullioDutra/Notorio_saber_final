from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Chamada, Feedback, AvaliacaoProfessor
from datetime import date
from acessos.models import Aluno,Professor
from django.core.paginator import Paginator
from django.db.models import Q

@login_required
def ver_aulas(request):
    aluno = get_object_or_404(Aluno, user=request.user)
    
    # Filtra aulas baseadas em presença
    aulas = Chamada.objects.filter(aluno=aluno, presente=True)
    
    # Pesquisa
    query = request.GET.get('search', '')
    if query:
        aulas = aulas.filter(
            Q(data__icontains=query) |
            Q(professor__user__first_name__icontains=query) |
            Q(professor__user__last_name__icontains=query)
        )
    
    # Paginação
    paginator = Paginator(aulas, 5)  # Mostra 5 aulas por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Cria uma lista de 1 a 5 para as estrelas
    estrelas = range(1, 6)

    return render(request, 'ver_aulas.html', {'page_obj': page_obj, 'estrelas': estrelas, 'search_query': query})

@login_required
def fornecer_feedback(request, chamada_id):
    chamada = get_object_or_404(Chamada, id=chamada_id, aluno__user=request.user)
    aluno_nome = chamada.aluno.user.get_full_name()  # Obtém o nome completo do aluno
    estrelas = range(1, 6)  # Cria uma lista de 1 a 5 para as estrelas

    if request.method == "POST":
        estrelas_feedback = int(request.POST.get('estrelas'))
        comentario = request.POST.get('comentario', '')

        Feedback.objects.create(
            chamada=chamada,
            estrelas=estrelas_feedback,
            comentario=comentario
        )

        messages.success(request, 'Feedback enviado com sucesso.')
        return redirect('ver_aulas')

    return render(request, 'fornecer_feedback.html', {'chamada': chamada, 'aluno_nome': aluno_nome, 'estrelas': estrelas})



@login_required
def listar_alunos_presentes(request):
    professor = get_object_or_404(Professor, user=request.user)
    query = request.GET.get('q')

    # Filtra as chamadas por professor e presença
    chamadas = Chamada.objects.filter(professor=professor, presente=True)

    # Filtra as chamadas pelo campo de pesquisa
    if query:
        chamadas = chamadas.filter(
            Q(aluno__user__first_name__icontains=query) |
            Q(aluno__user__last_name__icontains=query) |
            Q(data__icontains=query)
        )

    # Adiciona paginação
    paginator = Paginator(chamadas, 5)  # Mostra 5 chamadas por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    contexto = {
        'page_obj': page_obj,
        'estrelas': range(5),
        'query': query,
    }

    return render(request, 'listar_alunos_presentes.html', contexto)



@login_required
def listar_alunos_presentes_admin(request):
    professor = get_object_or_404(Professor, user=request.user)
    query = request.GET.get('q')

    # Filtra as chamadas por professor e presença
    chamadas = Chamada.objects.filter(professor=professor, presente=True)

    # Filtra as chamadas pelo campo de pesquisa
    if query:
        chamadas = chamadas.filter(
            Q(aluno__user__first_name__icontains=query) |
            Q(aluno__user__last_name__icontains=query) |
            Q(data__icontains=query)
        )

    # Adiciona paginação
    paginator = Paginator(chamadas, 5)  # Mostra 5 chamadas por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    contexto = {
        'page_obj': page_obj,
        'estrelas': range(5),
        'query': query,
    }

    return render(request, 'listar_alunos_presentes_admin.html', contexto)


def avaliar_aluno(request, chamada_id):
    chamada = get_object_or_404(Chamada, id=chamada_id, professor__user=request.user)

    if request.method == "POST":
        estrelas = int(request.POST.get('estrelas'))
        comentario = request.POST.get('comentario', '')

        AvaliacaoProfessor.objects.create(
            chamada=chamada,
            estrelas=estrelas,
            comentario=comentario
        )

        messages.success(request, 'Avaliação enviada com sucesso.')
        return redirect('listar_alunos_presentes')

    return render(request, 'avaliar_aluno.html', {'chamada': chamada})