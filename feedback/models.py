from django.db import models
from registros.models import Chamada

class Feedback(models.Model):
    chamada = models.OneToOneField(Chamada, on_delete=models.CASCADE)
    estrelas = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comentario = models.TextField(blank=True)

    def __str__(self):
        return f'Feedback for {self.chamada}'
    
    
class AvaliacaoProfessor(models.Model):
    chamada = models.OneToOneField(Chamada, on_delete=models.CASCADE)
    estrelas = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comentario = models.TextField(blank=True)

    def __str__(self):
        return f'Avaliação para {self.chamada}'
    