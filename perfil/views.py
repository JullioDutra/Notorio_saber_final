# perfil/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from rolepermissions.decorators import has_permission_decorator

@login_required
def perfil_admin(request):
    user = request.user
    return render(request, 'perfil_admin.html', {'user': user})


@login_required
def perfil_professor(request):
    user = request.user
    return render(request, 'perfil_professor.html', {'user': user})

@login_required
def perfil_aluno(request):
    user = request.user
    return render(request, 'perfil_aluno.html', {'user': user})
