from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from acessos.models import Aluno, Professor, Users
from registros.models import Chamada
from rolepermissions.decorators import has_permission_decorator
from datetime import datetime
from django.db.models import Count, Sum 
from django.db.models.functions import TruncMonth
from financeiro.models import Boleto
from calendario.models import Evento
from feedback.models import Feedback
from aulas_avulsas.models import AulaAvulsa
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from desempenho_aluno.models import Nota, DesempenhoAluno
from django.http import HttpResponseForbidden, HttpResponse
import csv

@login_required
def relatorio_aluno(request):
    alunos = Aluno.objects.all()
    aluno_selecionado = None
    if request.method == "POST":
        aluno_id = request.POST.get('aluno_id')
        aluno_selecionado = get_object_or_404(Aluno, id=aluno_id)

    return render(request, 'relatorio_aluno.html', {'alunos': alunos, 'aluno_selecionado': aluno_selecionado})


@login_required
def relatorio_arrecadacao_mensal(request):
    arrecadacao_mensal = {}

    # Obter todos os boletos pagos e usar a data de pagamento
    boletos_pagos = Boleto.objects.filter(pago=True)
    for boleto in boletos_pagos:
        # Assumindo que a data do boleto é armazenada em um campo chamado `data_pagamento`
        data_pagamento_date = boleto.mes_referencia  # Tipo datetime.date ou datetime.datetime
        mes_ano = data_pagamento_date.strftime('%Y-%m')

        if mes_ano not in arrecadacao_mensal:
            arrecadacao_mensal[mes_ano] = 0

        arrecadacao_mensal[mes_ano] += boleto.valor

    # Obter todas as aulas avulsas e usar a data da aula
    aulas_avulsas = AulaAvulsa.objects.all()
    for aula in aulas_avulsas:
        # Assumindo que a data da aula é armazenada em um campo chamado `data`
        data_aula_date = aula.data  # Tipo datetime.date ou datetime.datetime
        mes_ano = data_aula_date.strftime('%Y-%m')

        if mes_ano not in arrecadacao_mensal:
            arrecadacao_mensal[mes_ano] = 0

        arrecadacao_mensal[mes_ano] += aula.valor_aula * aula.quantidade_aulas

    # Ordenar os resultados por mês e ano
    arrecadacao_mensal = dict(sorted(arrecadacao_mensal.items()))

    return render(request, 'relatorio_arrecadacao_mensal.html', {'arrecadacao_mensal': arrecadacao_mensal})




@login_required
def relatorio_aulas_mensais_professor(request):
    professores = Professor.objects.all()
    relatorio = []

    for professor in professores:
        chamadas = Chamada.objects.filter(professor=professor).extra(select={'mes': "strftime('%%Y-%%m', data)"}).values('mes').annotate(total_aulas=Count('id')).order_by('mes')
        relatorio.append({'professor': professor, 'chamadas': chamadas})

    return render(request, 'relatorio_aulas_mensais_professor.html', {'relatorio': relatorio})


@login_required
def relatorio_pagamentos_pendentes(request):
    alunos = Aluno.objects.all()
    relatorio = []

    for aluno in alunos:
        boletos_pendentes = aluno.boletos.filter(pago=False)
        if boletos_pendentes.exists():
            # Construir a mensagem com as parcelas pendentes
            mensagens = []
            for boleto in boletos_pendentes:
                mensagens.append(f"Mês: {boleto.mes_referencia} - Valor: R$ {boleto.valor}")
            mensagem_texto = (
                f"Olá, {aluno.responsavel}. Você é o responsável pelo aluno {aluno.user.first_name} {aluno.user.last_name}. "
                f"Este é um lembrete sobre as seguintes parcelas pendentes:\n\n"
                f"{' '.join(mensagens)}\n\n"
                "Por favor, regularize o pagamento o mais breve possível. Obrigado!"
                f"Atenciosamente,\n\n"
                f"Equipe Notório Saber"
            )
            relatorio.append({'aluno': aluno, 'boletos_pendentes': boletos_pendentes, 'mensagem_texto': mensagem_texto})

    return render(request, 'relatorio_pagamentos_pendentes.html', {'relatorio': relatorio})

@login_required
def relatorio_pagamentos_realizados(request):
    alunos = Aluno.objects.all()
    relatorio = []

    for aluno in alunos:
        boletos_pagados = aluno.boletos.filter(pago=True)
        if boletos_pagados.exists():
            relatorio.append({'aluno': aluno, 'boletos_pagados': boletos_pagados})

    return render(request, 'relatorio_pagamentos_realizados.html', {'relatorio': relatorio})

@login_required
def relatorio_boletos_por_mes(request):
    boletos_por_mes = Boleto.objects.annotate(mes=TruncMonth('mes_referencia')).values('mes').annotate(
        total_boletos=Count('id'),
        total_valor=Sum('valor')
    ).order_by('mes')

    return render(request, 'relatorio_boletos_por_mes.html', {'boletos_por_mes': boletos_por_mes})


@login_required
def relatorio_planos_verificados(request):
    professores = Professor.objects.all()
    relatorio = []

    for professor in professores:
        planos_verificados = professor.checklist.filter(verificado=True)
        if planos_verificados.exists():
            relatorio.append({'professor': professor, 'planos_verificados': planos_verificados})

    return render(request, 'relatorio_planos_verificados.html', {'relatorio': relatorio})


@login_required
def relatorios_eventos(request):
    total_eventos = Evento.objects.count()
    eventos_por_tipo = Evento.objects.values('tipo').annotate(total=Count('tipo'))
    eventos_por_usuario = Users.objects.annotate(total_eventos=Count('eventos'))

    context = {
        'total_eventos': total_eventos,
        'eventos_por_tipo': eventos_por_tipo,
        'eventos_por_usuario': eventos_por_usuario,
    }

    return render(request, 'relatorios_eventos.html', context)


@login_required
def relatorio_feedback(request):
    feedbacks = Feedback.objects.select_related('chamada', 'chamada__aluno', 'chamada__professor')
    return render(request, 'relatorio_feedback.html', {'feedbacks': feedbacks})

@login_required
def relatorio_aulas_avulsas(request):
    aulas = AulaAvulsa.objects.all()

    # Preparar dados para os gráficos
    datas = [aula.data for aula in aulas]
    valores = [aula.valor_aula for aula in aulas]

    # Gráfico de barras
    plt.figure(figsize=(10, 5))
    plt.bar(datas, valores, color='blue')
    plt.xlabel('Data')
    plt.ylabel('Valor da Aula')
    plt.title('Valores das Aulas Avulsas por Data')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Salvar gráfico como uma imagem
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    graph_bars = base64.b64encode(image_png)
    graph_bars = graph_bars.decode('utf-8')

    # Limpar a figura atual
    plt.clf()

    # Gráfico de linha
    plt.figure(figsize=(10, 5))
    plt.plot(datas, valores, marker='o', linestyle='-', color='green')
    plt.xlabel('Data')
    plt.ylabel('Valor da Aula')
    plt.title('Tendência dos Valores das Aulas Avulsas')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Salvar gráfico como uma imagem
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    graph_line = base64.b64encode(image_png)
    graph_line = graph_line.decode('utf-8')

    context = {
        'graph_bars': graph_bars,
        'graph_line': graph_line,
    }

    return render(request, 'relatorio_aulas_avulsas.html', context)


@login_required
def relatorio_leitura(request):
    aluno = Aluno.objects.all()
    desempenhos = DesempenhoAluno.objects.filter(aluno=aluno).select_related('materia')
    
    desempenho_por_materia = {
        desempenho.materia.nome: {
            'media_aprovacao': desempenho.media_aprovacao,
            'notas': list(Nota.objects.filter(desempenho=desempenho).values_list('nota', flat=True)),
            'status': desempenho.desempenho_status()
        }
        for desempenho in desempenhos
    }
    
    return render(request, 'relatorio_leitura.html', {'desempenho_por_materia': desempenho_por_materia})


@login_required
def relatorio_aulas_reposicao(request):

    chamadas_reposicao = Chamada.objects.filter(precisa_reposicao=True).select_related('aluno', 'professor')

    context = {
        'chamadas_reposicao': chamadas_reposicao,
    }
    return render(request, 'relatorio_aulas_reposicao.html', context)


def exportar_aulas_reposicao_csv(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("Você não tem permissão para acessar esta página.")

    chamadas_reposicao = Chamada.objects.filter(precisa_reposicao=True).select_related('aluno', 'professor')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="aulas_reposicao.csv"'

    writer = csv.writer(response)
    writer.writerow(['Nome do Aluno', 'Nome do Professor', 'Data'])

    for chamada in chamadas_reposicao:
        writer.writerow([
            f"{chamada.aluno.user.first_name} {chamada.aluno.user.last_name}",
            f"{chamada.professor.user.first_name} {chamada.professor.user.last_name}",
            chamada.data
        ])

    return response