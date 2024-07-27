from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from acessos.models import Users
from .models import Mensagem
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta, datetime
from django.utils import timezone
from django.db.models import Max
from django.http import HttpResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import json


@login_required
def enviar_mensagem(request, destinatario_id):
    if request.method == 'POST':
        destinatario = get_object_or_404(Users, id=destinatario_id)
        conteudo = request.POST.get('conteudo')
        arquivo = request.FILES.get('arquivo')
        audio = request.FILES.get('audio')
        user = request.user
        
        if conteudo or arquivo or audio:
            Mensagem.objects.create(
                remetente=user,
                destinatario=destinatario,
                conteudo=conteudo,
                arquivo=arquivo,
                audio=audio
            )
            return redirect('conversa_atual', destinatario_id=destinatario_id)
        else:
            messages.error(request, "Você deve fornecer uma mensagem, arquivo ou áudio.")

    return redirect('conversa_atual', destinatario_id=destinatario_id)


    
@login_required
def conversa_atual(request, destinatario_id):
    contatos = Users.objects.exclude(id=request.user.id)
    destinatario = get_object_or_404(Users, id=destinatario_id)
    mensagens_enviadas = Mensagem.objects.filter(remetente=request.user, destinatario=destinatario)
    mensagens_recebidas = Mensagem.objects.filter(remetente=destinatario, destinatario=request.user)
    
    # Marcar mensagens recebidas como visualizadas
    mensagens_recebidas.update(visualizado=True)

    todas_mensagens = sorted(list(mensagens_enviadas) + list(mensagens_recebidas), key=lambda x: x.data_envio)

    
    
    extensoes_imagem = ['png', 'jpg', 'jpeg', 'gif']
    
        # Consulta ao banco de dados para recuperar os contatos ordenados pela data da última mensagem recebida
    contatos_ordenados = Users.objects.exclude(id=request.user.id).annotate(
        ultima_mensagem=Max('mensagens_recebidas__data_envio')
    ).order_by('-ultima_mensagem')

    
    return render(request, 'conversa_atual.html', {'destinatario': destinatario, 'mensagens': todas_mensagens, 'contatos': contatos, 'extensoes_imagem': extensoes_imagem, 'contatos_ordenados': contatos_ordenados})

@login_required
def lista_contatos(request):
    contatos = Users.objects.exclude(id=request.user.id)
    return render(request, 'contatos.html', {'contatos': contatos})

@login_required
def iniciar_conversa(request, destinatario_id):
    return redirect('conversa_atual', destinatario_id=destinatario_id)





def recuperar_novas_mensagens(request):
    if request.method == 'GET' and request.is_ajax():
        ultima_mensagem_visualizada = request.GET.get('ultima_mensagem_visualizada')
        
        if ultima_mensagem_visualizada:
            novas_mensagens = Mensagem.objects.filter(destinatario=request.user, visualizado=False, id__gt=ultima_mensagem_visualizada)
        else:
            novas_mensagens = Mensagem.objects.filter(destinatario=request.user, visualizado=False)
        
        novas_mensagens.update(visualizado=True)
        
        data = [{'id': mensagem.id, 'remetente': mensagem.remetente.username, 'conteudo': mensagem.conteudo, 'data_envio': mensagem.data_envio} for mensagem in novas_mensagens]
        return JsonResponse({'novas_mensagens': data})
    else:
        return JsonResponse({'error': 'Método não permitido ou requisição inválida'}, status=405)
    
    
def recuperar_contagem_nao_visualizadas(request):
    if request.method == 'GET':
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            contagens_nao_visualizadas = {}

            # Obter todos os contatos, exceto o usuário atual
            contatos = Users.objects.exclude(id=request.user.id)
            for contato in contatos:
                # Contar mensagens não visualizadas
                contagem = Mensagem.objects.filter(remetente=contato, destinatario=request.user, visualizado=False).count()
                contagens_nao_visualizadas[contato.id] = contagem

            data = {
                'contagens_nao_visualizadas': contagens_nao_visualizadas
            }
            return JsonResponse(data)
        else:
            return JsonResponse({'error': 'Método não permitido'}, status=405)
    else:
        return JsonResponse({'error': 'Método não permitido'}, status=405)


