from django.shortcuts import render
from django.shortcuts import render
from django.db.models import Count, Sum, F
from django.utils.timezone import now
from acessos.models import Professor,Aluno, Administrador
from . models import CarouselImage
from rolepermissions.decorators import has_permission_decorator
from avisos.models import Aviso
from calendario.models import Evento
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt
import base64
from io import BytesIO
from datetime import datetime, timedelta, timezone
from financeiro.models import Boleto
from aulas_avulsas.models import AulaAvulsa
from registros.models import Chamada
from feedback.models import Feedback
from django.shortcuts import render, get_object_or_404
from desempenho_aluno.models import Nota, DesempenhoAluno
from acessos.models import Users


def pagina_inicial_professor(request):
    carousel_images = CarouselImage.objects.all()
    avisos = Aviso.objects.all()
    eventos = Evento.objects.all()
    return render(request, 'dashboard_professor.html', {'carousel_images': carousel_images,'avisos':avisos, 'eventos':eventos})





def pagina_inicial_admin(request):
    
    context = {
        'relatorio_total_usuarios': relatorio_total_usuarios(),
        'relatorio_aulas_por_aluno': relatorio_aulas_por_aluno(),
        'relatorio_pagamentos_atrasados': relatorio_pagamentos_atrasados(),
        'relatorio_financeiro': relatorio_financeiro(),
        'relatorio_provisao': relatorio_provisao(),
        'relatorio_arrecadacao_mes':relatorio_arrecadacao_mes(),
        'relatorio_aulas_total':relatorio_aulas_total(),
        'relatorio_feedback':relatorio_feedback(),
    
    }
    return render(request, 'dashboard_admin.html', context)




def pagina_inicial_aluno(request):
    carousel_images = CarouselImage.objects.all()
    avisos = Aviso.objects.all()
    eventos = Evento.objects.all()
    return render(request, 'dashboard_aluno.html', {'carousel_images': carousel_images,'avisos':avisos, 'eventos':eventos})





def relatorio_total_usuarios():
    total_alunos = Aluno.objects.count()
    total_professores = Professor.objects.count()
    total_administradores = Administrador.objects.count()
    return {
        'total_alunos': total_alunos,
        'total_professores': total_professores,
        'total_administradores': total_administradores,
    }

def relatorio_aulas_por_aluno():
    alunos = Aluno.objects.annotate(total_aulas=Count('modalidade'))
    relatorio = [{'aluno': aluno.user.get_full_name(), 'total_aulas': aluno.total_aulas} for aluno in alunos]
    return relatorio

def relatorio_pagamentos_atrasados():
    hoje = now().date()
    
    # Buscar boletos não pagos e cujo prazo já passou
    boletos_atrasados = Boleto.objects.filter(
        pago=False,
        mes_referencia__lt=hoje
    )
    
    alunos = set(boletos_atrasados.values_list('aluno', flat=True))
    
    relatorio = []
    for aluno in alunos:
        aluno_obj = Aluno.objects.get(id=aluno)
        boletos = boletos_atrasados.filter(aluno=aluno)
        valor_total = boletos.aggregate(Sum('valor'))['valor__sum'] or 0
        relatorio.append({
            'aluno': aluno_obj.user.get_full_name(),
            'dia_pagamento': aluno_obj.dia_pagamento,
            'valor_total': valor_total,
            'total_ja_pago': aluno_obj.total_ja_pago
        })
    
    return relatorio


def relatorio_financeiro():
    hoje = now().date()

    # Total recebido
    total_recebido = Boleto.objects.filter(pago=True).aggregate(total_recebido=Sum('valor'))['total_recebido'] or 0

    # Total pendente
    total_pendente = Boleto.objects.filter(
        pago=False,
        mes_referencia__lt=hoje
    ).aggregate(total_pendente=Sum('valor'))['total_pendente'] or 0

    return {
        'total_recebido': total_recebido,
        'total_pendente': total_pendente,
    }




def relatorio_provisao():
    alunos = Aluno.objects.filter(is_active=True)
    
    # Preparar dados para os gráficos
    hoje = datetime.today().date()
    meses_futuros = 12  # Mostrar os próximos 12 meses
    valores_a_receber = {}

    for i in range(meses_futuros):
        mes = (hoje + relativedelta(months=i)).strftime('%Y-%m')
        valores_a_receber[mes] = 0

    for aluno in alunos:
        data_inicio = aluno.dia_pagamento
        data_fim = aluno.dia_pagamento + relativedelta(months=aluno.total_meses)
        mensalidade = aluno.mensalidade

        # Verificar se o contrato do aluno se sobrepõe ao período analisado
        if data_fim >= hoje:
            while data_inicio <= data_fim:
                mes_pagamento = data_inicio.strftime('%Y-%m')
                if mes_pagamento in valores_a_receber:
                    valores_a_receber[mes_pagamento] += mensalidade
                data_inicio += relativedelta(months=1)

    meses = list(valores_a_receber.keys())
    valores = list(valores_a_receber.values())

    # Gráfico de linha
    plt.figure(figsize=(10, 5))
    plt.plot(meses, valores, marker='o', linestyle='-', color='#f58634')
    plt.xlabel('Mês')
    plt.ylabel('Valor a Receber')
    plt.title('Provisão dos Valores a Receber nos Próximos Meses')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Salvar gráfico como uma imagem
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    graph_provisao = base64.b64encode(image_png)
    graph_provisao = graph_provisao.decode('utf-8')

    return graph_provisao


def relatorio_arrecadacao_mes():
    hoje = now().date()
    inicio_do_mes_atual = hoje.replace(day=1)
    fim_do_mes_atual = hoje.replace(day=1) + timedelta(days=31)
    fim_do_mes_atual = fim_do_mes_atual.replace(day=1) - timedelta(days=1)
    
    # Total arrecadado com boletos pagos no mês atual
    total_boletos_pagos = Boleto.objects.filter(
        pago=True,
        mes_referencia__range=[inicio_do_mes_atual, fim_do_mes_atual]
    ).aggregate(total_boletos=Sum('valor'))['total_boletos'] or 0
    
    # Total arrecadado com aulas avulsas no mês atual
    total_aulas_avulsas = AulaAvulsa.objects.filter(
        data__range=[inicio_do_mes_atual, fim_do_mes_atual]
    ).aggregate(total_aulas=Sum('valor_aula'))['total_aulas'] or 0

    return {
        'total_boletos_pagos': total_boletos_pagos,
        'total_aulas_avulsas': total_aulas_avulsas,
        'total_arrecadado': total_boletos_pagos + total_aulas_avulsas
    }
    
def relatorio_aulas_total():
    hoje = now().date()
    inicio_do_mes_atual = hoje.replace(day=1)
    fim_do_mes_atual = (inicio_do_mes_atual + timedelta(days=31)).replace(day=1) - timedelta(days=1)

    # Contar o total de aulas registradas no mês atual
    total_aulas_registradas = Chamada.objects.filter(data__range=[inicio_do_mes_atual, fim_do_mes_atual]).count()

    # Somar o total de aulas avulsas no mês atual
    total_aulas_avulsas = AulaAvulsa.objects.filter(data__range=[inicio_do_mes_atual, fim_do_mes_atual]).aggregate(total_aulas=Sum('quantidade_aulas'))['total_aulas'] or 0

    # Calcular o total de aulas no mês
    total_aulas = total_aulas_registradas + total_aulas_avulsas

    return {
        'total_aulas': total_aulas,
    }
    

def relatorio_feedback():
    feedbacks = Feedback.objects.all()

    # Contar feedbacks por número de estrelas
    contagem_feedbacks = {
        'Ótimo': feedbacks.filter(estrelas=5).count(),
        'Bom': feedbacks.filter(estrelas=4).count(),
        'Regular': feedbacks.filter(estrelas=3).count(),
        'Ruim': feedbacks.filter(estrelas=2).count(),
        'Muito ruim': feedbacks.filter(estrelas=1).count(),
    }

    # Dados para o gráfico
    labels = list(contagem_feedbacks.keys())
    valores = list(contagem_feedbacks.values())

    # Criar o gráfico
    plt.figure(figsize=(10, 5))
    plt.bar(labels, valores, color=['green', 'blue', 'yellow', 'orange', 'red'])
    plt.xlabel('Feedback')
    plt.ylabel('Quantidade')
    plt.title('Distribuição de Feedback dos Alunos')
    plt.tight_layout()

    # Salvar gráfico como uma imagem
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    graph_bars = base64.b64encode(image_png)
    graph_bars = graph_bars.decode('utf-8')



    return graph_bars



def relatorio_grafico():
    aluno = Aluno.objects.all()
    desempenhos = DesempenhoAluno.objects.filter(aluno=aluno).select_related('materia')
    
    materias = [desempenho.materia.nome for desempenho in desempenhos]
    medias_aprovacao = [desempenho.media_aprovacao for desempenho in desempenhos]
    
    # Criação do gráfico
    fig, ax = plt.subplots()
    ax.bar(materias, medias_aprovacao, color='skyblue')
    ax.set_xlabel('Matérias')
    ax.set_ylabel('Média de Aprovação')
    ax.set_title('Desempenho por Matéria')

    # Salvando o gráfico em uma imagem base64
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()
    
    return image_base64