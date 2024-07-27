from django.db import models
from acessos.models import Aluno, Professor

class Chamada(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    data = models.DateField()
    presente = models.BooleanField()
    precisa_reposicao = models.BooleanField(default=False)