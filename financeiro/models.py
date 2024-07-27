from django.db import models
from acessos.models import Aluno


class Boleto(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='boletos')
    mes_referencia = models.DateField()
    arquivo = models.FileField(upload_to='boletos/')
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    pago = models.BooleanField(default=False)
    chave_pix = models.CharField(max_length=100, blank=True, null=True)  # Adicione este campo
    link_pagamento = models.URLField(blank=True, null=True)  # Novo campo para o link de pagamento
    qr_code_pix = models.ImageField(upload_to='qrcodes_pix/', blank=True, null=True)  # Novo campo para o QR code do Pix

    def __str__(self):
        return f"Boleto {self.mes_referencia} - {self.aluno.user.get_full_name()}"

class ComprovantePagamento(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='comprovantes')
    boleto = models.ForeignKey(Boleto, on_delete=models.CASCADE, related_name='comprovantes')
    data_envio = models.DateTimeField(auto_now_add=True)
    arquivo = models.FileField(upload_to='comprovantes/')

    def __str__(self):
        return f"Comprovante de {self.aluno.user.get_full_name()} para {self.boleto.mes_referencia}"


