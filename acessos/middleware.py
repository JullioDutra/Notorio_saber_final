from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from acessos.models import Aluno, Professor

class CheckActiveUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            user = request.user
            if user.cargo == 'S':
                aluno = Aluno.objects.filter(user=user).first()
                if aluno and not aluno.is_active:
                    messages.error(request, 'Sua conta está inativa. Entre em contato com o administrador.')
                    return redirect(reverse('logout'))
            elif user.cargo == 'P':
                professor = Professor.objects.filter(user=user).first()
                if professor and not professor.is_active:
                    messages.error(request, 'Sua conta está inativa. Entre em contato com o administrador.')
                    return redirect(reverse('logout'))

        response = self.get_response(request)
        return response
