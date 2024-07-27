from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from .models import Users, Aluno, Modalidade, Professor
from datetime import datetime
from dateutil.relativedelta import relativedelta
from rolepermissions.decorators import has_permission_decorator
from django.contrib.auth import logout as auth_logout

@login_required
def cadastrar_aluno(request):
    if request.method == "GET":
        modalidades = Modalidade.objects.all()
        professores = Professor.objects.all()
        return render(request, 'cadastrar_aluno.html', {'modalidades': modalidades, 'professores': professores})

    if request.method == "POST":
        nome = request.POST.get('nome')
        sobrenome = request.POST.get('sobrenome')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        responsavel = request.POST.get('responsavel')
        contato = request.POST.get('contato')
        modalidade_id = request.POST.get('modalidade')
        quantidade_aulas = int(request.POST.get('quantidade_aulas'))
        dia_pagamento = request.POST.get('dia_pagamento')
        mensalidade = float(request.POST.get('mensalidade'))
        total_ja_pago = float(request.POST.get('total_ja_pago', 0))
        total_meses = int(request.POST.get('total_meses'))
        foto = request.FILES.get('foto')
        professores_ids = request.POST.getlist('professores')

        # Verifique se o usuário já existe
        if Users.objects.filter(email=email).exists():
            messages.error(request, 'Este usuário já existe.')
            return redirect(reverse('cadastrar_aluno'))

        try:
            # Crie o usuário
            user = Users.objects.create_user(
                username=email,
                email=email,
                password=senha,
                first_name=nome,
                last_name=sobrenome,
                cargo='S'
            )

            # Obtenha a modalidade
            modalidade = Modalidade.objects.get(id=modalidade_id)

            # Calcule o valor total
            valor_total = mensalidade * quantidade_aulas

            # Converta dia_pagamento para um objeto datetime
            dia_pagamento_date = datetime.strptime(dia_pagamento, '%Y-%m-%d').date()

            # Calcule a data de fim do contrato
            fim_contrato = dia_pagamento_date + relativedelta(months=total_meses)

            # Crie o aluno
            aluno = Aluno.objects.create(
                user=user,
                responsavel=responsavel,
                contato=contato,
                modalidade=modalidade,
                quantidade_aulas=quantidade_aulas,
                aulas_restante=quantidade_aulas,  # Inicialmente, aulas restantes igual a quantidade de aulas
                dia_pagamento=dia_pagamento_date,
                fim_contrato=fim_contrato,
                valor_total=valor_total,
                mensalidade=mensalidade,
                total_ja_pago=total_ja_pago,
                foto=foto,
                total_meses=total_meses
            )

            # Calcule e atualize as datas de pagamento
            aluno.calcular_datas_pagamento()
            aluno.save()

            # Vincule os professores ao aluno
            for professor_id in professores_ids:
                professor = Professor.objects.get(id=professor_id)
                professor.alunos.add(aluno)

            messages.success(request, 'Aluno cadastrado com sucesso.')
            return redirect(reverse('cadastrar_aluno'))
        except Exception as e:
            messages.error(request, f'Ocorreu um erro: {e}')
            return redirect(reverse('cadastrar_aluno'))


@login_required
def cadastrar_professor(request):
    if request.method == "GET":
        alunos = Aluno.objects.all()
        return render(request, 'cadastrar_professor.html', {'alunos': alunos})

    if request.method == "POST":
        nome = request.POST.get('nome')
        sobrenome = request.POST.get('sobrenome')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        foto = request.FILES.get('foto')
        aluno_ids = request.POST.getlist('alunos')

        # Verifique se o usuário já existe
        user_exists = Users.objects.filter(email=email).exists()
        if user_exists:
            messages.error(request, 'Este usuário já existe.')
            return redirect(reverse('cadastrar_professor'))

        # Crie o usuário
        user = Users.objects.create_user(
            username=email,
            email=email,
            password=senha,
            first_name=nome,
            last_name=sobrenome,
            cargo='P'
        )

        # Verifique se o usuário já tem um perfil de professor
        if not hasattr(user, 'professor'):
            # Crie o professor
            professor = Professor.objects.create(user=user, foto=foto)
        else:
            professor = user.professor

        # Vincule os alunos ao professor
        for aluno_id in aluno_ids:
            aluno = Aluno.objects.get(id=aluno_id)
            professor.alunos.add(aluno)

        messages.success(request, 'Professor cadastrado com sucesso.')
        return redirect(reverse('cadastrar_professor'))

def login(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect_user_by_role(request.user)
        return render(request, 'login.html')
    elif request.method == "POST":
        login = request.POST.get('email')
        senha = request.POST.get('senha')

        user = auth.authenticate(username=login, password=senha)

        if user is not None:
            auth.login(request, user)
            messages.add_message(request, messages.SUCCESS, 'usuário logado')
            return redirect_user_by_role(user)
        else:
            messages.add_message(request, messages.ERROR, 'usuário invalido')
            return redirect(reverse('login'))

def redirect_user_by_role(user):
    if user.cargo == 'A':
        return redirect(reverse('dashboard_admin'))  # substitua 'admin_dashboard' pela URL da dashboard do administrador
    elif user.cargo == 'S':
        return redirect(reverse('dashboard_aluno'))  # substitua 'student_dashboard' pela URL da dashboard do aluno
    elif user.cargo == 'P':
        return redirect(reverse('dashboard_professsor'))  # substitua 'teacher_dashboard' pela URL da dashboard do professor
    else:
        return redirect(reverse('login'))

def logout(request):
    auth_logout(request)
    messages.success(request, 'Você saiu com sucesso.')
    return redirect(reverse('login'))




def excluir_usuario(request, id):
    aluno = get_object_or_404(Aluno, user__id=id)
    aluno.delete()
    messages.add_message(request, messages.SUCCESS, 'Usuário excluído com sucesso')
    return redirect(reverse('cadastrar_usuarios'))

@login_required
def listar_usuarios(request):
    if request.user.cargo != 'A':
        messages.error(request, 'Você não tem permissão para acessar esta página.')
        return redirect('dashboard_admin')
    
    alunos = Aluno.objects.all()
    professores = Professor.objects.all()
    return render(request, 'listar_usuarios.html', {'alunos': alunos, 'professores': professores})

@login_required
def inativar_aluno(request, aluno_id):
    if request.user.cargo != 'A':
        messages.error(request, 'Você não tem permissão para acessar esta página.')
        return redirect('dashboard_admin')

    aluno = get_object_or_404(Aluno, id=aluno_id)
    aluno.is_active = False
    aluno.save()
    messages.success(request, 'Aluno inativado com sucesso.')
    return redirect('listar_usuarios')

@login_required
def ativar_aluno(request, aluno_id):
    if request.user.cargo != 'A':
        messages.error(request, 'Você não tem permissão para acessar esta página.')
        return redirect('dashboard_admin')

    aluno = get_object_or_404(Aluno, id=aluno_id)
    aluno.is_active = True
    aluno.save()
    messages.success(request, 'Aluno ativado com sucesso.')
    return redirect('listar_usuarios')

@login_required
def inativar_professor(request, professor_id):
    if request.user.cargo != 'A':
        messages.error(request, 'Você não tem permissão para acessar esta página.')
        return redirect('dashboard_admin')

    professor = get_object_or_404(Professor, id=professor_id)
    professor.is_active = False
    professor.save()
    messages.success(request, 'Professor inativado com sucesso.')
    return redirect('listar_usuarios')

@login_required
def ativar_professor(request, professor_id):
    if request.user.cargo != 'A':
        messages.error(request, 'Você não tem permissão para acessar esta página.')
        return redirect('dashboard_admin')

    professor = get_object_or_404(Professor, id=professor_id)
    professor.is_active = True
    professor.save()
    messages.success(request, 'Professor ativado com sucesso.')
    return redirect('listar_usuarios')