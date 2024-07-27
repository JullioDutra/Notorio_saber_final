from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import DesempenhoAluno, Materia, Nota
from acessos.models import Users

@login_required
def configurar_desempenho(request):
    aluno = get_object_or_404(Users, id=request.user.id)
    if request.method == 'POST':
        materia_id = request.POST.get('materia')
        media_aprovacao = float(request.POST.get('media_aprovacao'))
        materia = get_object_or_404(Materia, id=materia_id)
        DesempenhoAluno.objects.update_or_create(
            aluno=aluno, materia=materia, defaults={'media_aprovacao': media_aprovacao}
        )
        messages.success(request, 'Média de aprovação configurada com sucesso.')
        return redirect('ver_desempenho')

    materias = Materia.objects.all()
    return render(request, 'configurar_desempenho.html', {'materias': materias})

@login_required
def adicionar_nota(request):
    aluno = get_object_or_404(Users, id=request.user.id)
    if request.method == 'POST':
        materia_id = request.POST.get('materia')
        nota = float(request.POST.get('nota'))
        materia = get_object_or_404(Materia, id=materia_id)
        desempenho, created = DesempenhoAluno.objects.get_or_create(
            aluno=aluno, materia=materia
        )
        Nota.objects.create(desempenho=desempenho, materia=materia, nota=nota)
        messages.success(request, 'Nota adicionada com sucesso.')
        return redirect('ver_desempenho')

    materias = Materia.objects.all()
    return render(request, 'adicionar_nota.html', {'materias': materias})

@login_required
def ver_desempenho(request):
    aluno = get_object_or_404(Users, id=request.user.id)
    desempenhos = DesempenhoAluno.objects.filter(aluno=aluno).select_related('materia')
    notas = Nota.objects.filter(desempenho__in=desempenhos).order_by('materia', 'data')
    
    desempenho_por_materia = {}
    
    for desempenho in desempenhos:
        notas_materia = notas.filter(materia=desempenho.materia)
        
        if notas_materia.exists():
            notas_lista = list(notas_materia)
            notas_ordenadas = sorted(notas_lista, key=lambda x: x.data)
            comparacoes = []
            
            for i in range(1, len(notas_ordenadas)):
                nota_atual = notas_ordenadas[i]
                nota_anterior = notas_ordenadas[i-1]
                
                if nota_atual.nota > nota_anterior.nota:
                    comparacao = 'Melhorou'
                elif nota_atual.nota < nota_anterior.nota:
                    comparacao = 'Piorou'
                else:
                    comparacao = 'Mesmo'
                
                comparacoes.append({
                    'nota': nota_atual.nota,
                    'data': nota_atual.data,
                    'comparacao': comparacao
                })
            
            # Adiciona a última nota (sem comparação)
            comparacoes.append({
                'nota': notas_ordenadas[-1].nota,
                'data': notas_ordenadas[-1].data,
                'comparacao': 'N/A'
            })
            
            desempenho_por_materia[desempenho.materia] = {
                'media_aprovacao': desempenho.media_aprovacao,
                'notas': comparacoes,
                'status': desempenho.desempenho_status()
            }
    
    return render(request, 'ver_desempenho.html', {'desempenho_por_materia': desempenho_por_materia})

