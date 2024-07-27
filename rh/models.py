from django.db import models

class Presenca(models.Model):
    nome = models.CharField(max_length=100)
    data = models.DateField()
    departamento = models.CharField(max_length=255)
    ausencia_dias = models.PositiveIntegerField(default=0)
    pedido_licenca_dias = models.PositiveIntegerField(default=0)
    viagem_dias = models.PositiveIntegerField(default=0)
    entrada_dias = models.PositiveIntegerField(default=0)
    horas_extra = models.PositiveIntegerField(default=0)
    atraso = models.PositiveIntegerField(default=0)
    sair_cedo = models.PositiveIntegerField(default=0)
    # Adicione outros campos conforme necessário

    def __str__(self):
        return f"{self.nome} - {self.data}"
