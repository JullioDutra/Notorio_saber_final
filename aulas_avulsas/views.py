from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import AulaAvulsa

@login_required
def registrar_aula_avulsa(request):
    if request.method == "POST":
        data = request.POST.get('data')
        nome_aluno = request.POST.get('nome_aluno')
        responsavel = request.POST.get('responsavel')
        valor_aula = request.POST.get('valor_aula')
        quantidade_aulas = request.POST.get('quantidade_aulas')
        observacoes = request.POST.get('observacoes')

        AulaAvulsa.objects.create(
            data=data,
            nome_aluno=nome_aluno,
            responsavel=responsavel,
            valor_aula=valor_aula,
            quantidade_aulas=quantidade_aulas,
            observacoes=observacoes
        )

        messages.success(request, 'Aula avulsa registrada com sucesso.')
        return redirect('listar_aulas_avulsas')

    return render(request, 'registrar_aula_avulsa.html')

@login_required
def registrar_aula_avulsa_admin(request):
    if request.method == "POST":
        data = request.POST.get('data')
        nome_aluno = request.POST.get('nome_aluno')
        responsavel = request.POST.get('responsavel')
        valor_aula = request.POST.get('valor_aula')
        quantidade_aulas = request.POST.get('quantidade_aulas')
        observacoes = request.POST.get('observacoes')

        AulaAvulsa.objects.create(
            data=data,
            nome_aluno=nome_aluno,
            responsavel=responsavel,
            valor_aula=valor_aula,
            quantidade_aulas=quantidade_aulas,
            observacoes=observacoes
        )

        messages.success(request, 'Aula avulsa registrada com sucesso.')
        return redirect('listar_aulas_avulsas')

    return render(request, 'registrar_aula_avulsa_admin.html')

@login_required
def listar_aulas_avulsas(request):
    aulas_avulsas = AulaAvulsa.objects.all()
    return render(request, 'listar_aulas_avulsas.html', {'aulas_avulsas': aulas_avulsas})

@login_required
def listar_aulas_avulsas_admin(request):
    aulas_avulsas = AulaAvulsa.objects.all()
    return render(request, 'listar_aulas_avulsas_admin.html', {'aulas_avulsas': aulas_avulsas})