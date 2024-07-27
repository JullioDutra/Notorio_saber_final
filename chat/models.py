from django.db import models
from acessos.models import Users

    
class Mensagem(models.Model):
    remetente = models.ForeignKey(Users, related_name='mensagens_enviadas', on_delete=models.CASCADE)
    destinatario = models.ForeignKey(Users, related_name='mensagens_recebidas', on_delete=models.CASCADE)
    conteudo = models.TextField(blank=True, null=True)
    arquivo = models.FileField(upload_to='media/imagens', blank=True, null=True)
    data_envio = models.DateTimeField(auto_now_add=True)
    visualizado = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.remetente} para {self.destinatario} - {self.conteudo[:20]}'
    
    class Meta:
        ordering = ['-data_envio']  # Ordenar as mensagens pela data de envio, mais recente primeiro
    
    
    
    
class Contato(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='contatos')
    contato = models.ForeignKey(Users, on_delete=models.CASCADE)