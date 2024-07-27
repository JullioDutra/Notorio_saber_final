from django.db import models
from acessos.models import Users


class Evento(models.Model):
    EVENT_TYPE_CHOICES = (
        ('R', 'Recesso'),
        ('F', 'Feriado'),
        ('A', 'Aula')
    )

    titulo = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    tipo = models.CharField(max_length=1, choices=EVENT_TYPE_CHOICES)
    data_inicio = models.DateTimeField()
    data_fim = models.DateTimeField()
    usuarios_destinados = models.ManyToManyField(Users, blank=True, related_name='eventos')

    def __str__(self):
        return self.titulo