# aulas_avulsas/models.py
from django.db import models

class AulaAvulsa(models.Model):
    data = models.DateField()
    nome_aluno = models.CharField(max_length=255)
    responsavel = models.CharField(max_length=255)
    valor_aula = models.DecimalField(max_digits=10, decimal_places=2)
    quantidade_aulas = models.PositiveIntegerField()
    observacoes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.nome_aluno} - {self.data}"
