from django.db import models
from acessos.models import Aluno, Professor

class PlanoAula(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='planos')
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    arquivo = models.FileField(upload_to='planos_aula/', null=True, blank=True)
    data_criacao = models.DateTimeField(auto_now_add=True)

class ChecklistProfessor(models.Model):
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE, related_name='checklist')
    plano_aula = models.ForeignKey(PlanoAula, on_delete=models.CASCADE)
    verificado = models.BooleanField(default=False)
    data_verificacao = models.DateTimeField(null=True, blank=True)
    
    