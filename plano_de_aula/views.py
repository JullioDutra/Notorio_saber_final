from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from rolepermissions.decorators import has_permission_decorator
from django.utils import timezone
from .models import Aluno, Professor, PlanoAula, ChecklistProfessor
from .forms import PlanoAulaForm
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q

@login_required
def criar_plano_aula(request):
    aluno = get_object_or_404(Aluno, user=request.user)

    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        descricao = request.POST.get('descricao')
        arquivo = request.FILES.get('arquivo')

        if titulo and descricao and arquivo:
            plano = PlanoAula(titulo=titulo, descricao=descricao, arquivo=arquivo, aluno=aluno)
            plano.save()
            return redirect('criar_plano_aula')  # Redireciona para a mesma página para evitar resubmissão do formulário
        else:
            # Adiciona uma mensagem de erro se algum campo estiver faltando
            messages.error(request, 'Por favor, preencha todos os campos e faça o upload do arquivo.')

    # Obtém os planos já criados pelo aluno
    planos = PlanoAula.objects.filter(aluno=aluno)
    return render(request, 'criar_plano_aula.html', {'planos': planos})


@login_required
def listar_planos_aula(request):
    try:
        professor = Professor.objects.get(user=request.user)
    except Professor.DoesNotExist:
        return HttpResponseForbidden("Você não tem permissão para acessar esta página.")

    # Filtrar planos de aula com base no título
    query = request.GET.get('q')
    if query:
        planos = PlanoAula.objects.filter(Q(aluno__in=professor.alunos.all()) & Q(titulo__icontains=query))
    else:
        planos = PlanoAula.objects.filter(aluno__in=professor.alunos.all())

    # Adicionar a informação de verificado a cada plano
    planos_verificados = []
    for plano in planos:
        verificado = plano.checklistprofessor_set.filter(professor=professor, verificado=True).exists()
        planos_verificados.append({
            'plano': plano,
            'verificado': verificado
        })

    # Paginação
    paginator = Paginator(planos_verificados, 5)  # 5 planos por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'listar_planos_aula.html', {'page_obj': page_obj, 'professor': professor, 'query': query})


@login_required
def listar_planos_aula_admin(request):
    try:
        professor = Professor.objects.get(user=request.user)
    except Professor.DoesNotExist:
        return HttpResponseForbidden("Você não tem permissão para acessar esta página.")

    # Filtrar planos de aula com base no título
    query = request.GET.get('q')
    if query:
        planos = PlanoAula.objects.filter(Q(aluno__in=professor.alunos.all()) & Q(titulo__icontains=query))
    else:
        planos = PlanoAula.objects.filter(aluno__in=professor.alunos.all())

    # Adicionar a informação de verificado a cada plano
    planos_verificados = []
    for plano in planos:
        verificado = plano.checklistprofessor_set.filter(professor=professor, verificado=True).exists()
        planos_verificados.append({
            'plano': plano,
            'verificado': verificado
        })

    # Paginação
    paginator = Paginator(planos_verificados, 5)  # 5 planos por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'listar_planos_aula_admin.html', {'page_obj': page_obj, 'professor': professor, 'query': query})


@login_required
def verificar_plano_aula(request, plano_id):
    professor = get_object_or_404(Professor, user=request.user)
    plano = get_object_or_404(PlanoAula, id=plano_id)

    if plano.aluno not in professor.alunos.all():
        return HttpResponseForbidden("Você não tem permissão para verificar este plano de aula.")

    checklist, created = ChecklistProfessor.objects.get_or_create(professor=professor, plano_aula=plano)
    checklist.verificado = not checklist.verificado
    if checklist.verificado:
        checklist.data_verificacao = timezone.now()
    else:
        checklist.data_verificacao = None
    checklist.save()

    return redirect('listar_planos_aula')
