from django.shortcuts import render, redirect
from django.contrib import messages
from rolepermissions.decorators import has_permission_decorator
from django.contrib.auth.decorators import login_required
from .models import Aluno, Boleto, ComprovantePagamento
from django.shortcuts import get_object_or_404
from .utils import gerar_qr_code_pix
from django.db.models import Sum
from django.core.paginator import Paginator
from django.db.models import Q


@login_required
def anexar_boleto(request):
    if request.method == "POST":
        aluno_id = request.POST.get('aluno_id')
        mes_referencia = request.POST.get('mes_referencia')
        valor = request.POST.get('valor')
        arquivo = request.FILES.get('arquivo')
        chave_pix = request.POST.get('chave_pix')
        link_pagamento = request.POST.get('link_pagamento')

        aluno = Aluno.objects.get(id=aluno_id)
        nome_recipiente = aluno.user.get_full_name()
        cidade = 'Cidade'  # Substitua pela cidade apropriada

        # Gera o QR code a partir da chave Pix
        qr_code_pix = gerar_qr_code_pix(
            chave_pix=chave_pix,
            nome_recipiente=nome_recipiente,
            cidade=cidade,
            valor=valor,
            identificador=mes_referencia
        )

        boleto = Boleto.objects.create(
            aluno=aluno,
            mes_referencia=mes_referencia,
            valor=valor,
            arquivo=arquivo,
            chave_pix=chave_pix,
            link_pagamento=link_pagamento,
            qr_code_pix=qr_code_pix
        )

        messages.success(request, 'Boleto anexado com sucesso.')
        return redirect('anexar_boleto')

    alunos = Aluno.objects.all()
    return render(request, 'anexar_boleto.html', {'alunos': alunos})





@login_required
def minha_financa(request):
    aluno = get_object_or_404(Aluno, user=request.user)
    boletos = aluno.boletos.all()

    # Pesquisa
    query = request.GET.get('search', '')
    if query:
        boletos = boletos.filter(
            mes_referencia__icontains=query
        )

    # Paginação
    paginator = Paginator(boletos, 5)  # Mostra 5 boletos por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.method == "POST":
        boleto_id = request.POST.get('boleto_id')
        arquivo = request.FILES.get('arquivo')

        boleto = Boleto.objects.get(id=boleto_id)
        ComprovantePagamento.objects.create(aluno=aluno, boleto=boleto, arquivo=arquivo)

        messages.success(request, 'Comprovante enviado com sucesso.')
        return redirect('minha_financa')

    return render(request, 'minha_financa.html', {'page_obj': page_obj, 'search_query': query})





@login_required
def validar_comprovante(request):
    query = request.GET.get('q')
    comprovantes = ComprovantePagamento.objects.filter(boleto__pago=False)

    if query:
        comprovantes = comprovantes.filter(
            Q(aluno__user__first_name__icontains=query) |
            Q(aluno__user__last_name__icontains=query) |
            Q(boleto__mes_referencia__icontains=query)
        )

    paginator = Paginator(comprovantes, 5)  # 5 comprovantes por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.method == "POST":
        comprovante_id = request.POST.get('comprovante_id')
        comprovante = ComprovantePagamento.objects.get(id=comprovante_id)
        comprovante.boleto.pago = True
        comprovante.boleto.save()

        # Atualizar o total pago pelo aluno
        aluno = comprovante.aluno
        total_pago = Boleto.objects.filter(aluno=aluno, pago=True).aggregate(Sum('valor'))['valor__sum']
        aluno.total_ja_pago = total_pago
        aluno.save()

        messages.success(request, 'Comprovante validado com sucesso.')
        return redirect('validar_comprovante')

    return render(request, 'validar_comprovante.html', {'page_obj': page_obj, 'query': query})
