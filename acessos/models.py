from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from dateutil.relativedelta import relativedelta
from datetime import timedelta

class Users(AbstractUser):
    choices_cargo = (('A', 'Administrador'),
                     ('S', 'Aluno'),
                     ('P', 'Professor'))
    cargo = models.CharField(max_length=1, choices=choices_cargo)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

class Modalidade(models.Model):
    titulo = models.CharField(max_length=25)

class Administrador(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE, related_name='administrador')
    foto = models.ImageField(null=True, blank=True)

class Aluno(models.Model):
    foto = models.ImageField()
    user = models.OneToOneField(Users, on_delete=models.CASCADE, related_name='aluno')
    responsavel = models.CharField(max_length=50)
    contato = models.CharField(max_length=15)  # Use CharField para permitir a formatação do número de telefone
    modalidade = models.ForeignKey(Modalidade, on_delete=models.CASCADE)
    quantidade_aulas = models.IntegerField()
    aulas_restante = models.IntegerField()
    dia_pagamento = models.DateField()
    data_inicio = models.DateField(auto_now_add=True)  # Data de início do contrato
    fim_contrato = models.DateField(editable=False)  # Data de término do contrato
    valor_total = models.FloatField(editable=False, null=True)  # Valor total, calculado automaticamente
    mensalidade = models.FloatField()
    total_ja_pago = models.FloatField(default=0.0)  # Total já pago
    contrato = models.FileField(upload_to="contratos", max_length=100)
    datas_pagamento = models.JSONField(default=list, editable=False)  # Campo para armazenar as datas de pagamento
    total_meses = models.IntegerField()
    is_active = models.BooleanField(default=True)
    professores = models.ManyToManyField('Professor', related_name='alunos_associados')

    def calcular_valor_total(self):
        return self.mensalidade * self.quantidade_aulas

    def atualizar_valor_total(self):
        self.valor_total = self.calcular_valor_total()

    def calcular_fim_contrato(self):
        if self.data_inicio:
            self.fim_contrato = self.data_inicio + relativedelta(months=self.quantidade_aulas)

    def calcular_datas_pagamento(self):
        datas_pagamento = []
        data_pagamento = self.dia_pagamento
        for _ in range(self.quantidade_aulas):
            datas_pagamento.append(data_pagamento.strftime('%Y-%m-%d'))
            data_pagamento += relativedelta(months=1)
        self.datas_pagamento = datas_pagamento

    def save(self, *args, **kwargs):
        self.atualizar_valor_total()
        self.calcular_fim_contrato()
        self.calcular_datas_pagamento()
        super().save(*args, **kwargs)

class Professor(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE, related_name='professor')
    foto = models.ImageField(upload_to='fotos_professor/', height_field=None, width_field=None, max_length=None)
    alunos = models.ManyToManyField('Aluno', related_name='professores_associados')
    is_active = models.BooleanField(default=True)

# Sinal para criar Aluno, Professor ou Administrador quando um usuário é salvo
@receiver(post_save, sender=Users)
def criar_perfil_usuario(sender, instance, created, **kwargs):
    if created:
        if instance.is_superuser and not hasattr(instance, 'professor'):
            Professor.objects.create(user=instance)
        elif instance.cargo == 'A' and not hasattr(instance, 'administrador'):
            Administrador.objects.create(user=instance)
        elif instance.cargo == 'S' and not hasattr(instance, 'aluno'):
            # O Aluno será criado com valores reais via a view
            pass
        elif instance.cargo == 'P' and not hasattr(instance, 'professor'):
            Professor.objects.create(user=instance)