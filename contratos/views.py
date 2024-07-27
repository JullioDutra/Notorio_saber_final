from django.shortcuts import render
from acessos.models import Aluno  # Verifique se está importando o modelo Aluno corretamente
from rolepermissions.decorators import has_permission_decorator
from django.core.paginator import Paginator
from django.db.models import Q


def contratos(request):
    query = request.GET.get('q', '')  # Campo de pesquisa
    alunos = Aluno.objects.filter(Q(user__first_name__icontains=query) | Q(user__last_name__icontains=query))

    paginator = Paginator(alunos, 6)  # 6 contratos por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'contratos.html', {'page_obj': page_obj, 'query': query})