from django.db import models
from django.db.models import Avg
from acessos.models import Users

class Materia(models.Model):
    nome = models.CharField(max_length=255)

    def __str__(self):
        return self.nome

class DesempenhoAluno(models.Model):
    aluno = models.OneToOneField(Users, on_delete=models.CASCADE)
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    media_aprovacao = models.FloatField()

    def __str__(self):
        return f'{self.aluno} - {self.materia}'

    def desempenho_status(self):
        # Calcula a média das notas para a matéria
        media_notas = Nota.objects.filter(desempenho=self, materia=self.materia).aggregate(Avg('nota'))['nota__avg']
        
        # Verifica se há notas registradas
        if media_notas is None:
            return 'Sem Notas'

        # Determina o status do desempenho
        if media_notas >= self.media_aprovacao:
            return 'Melhorou'
        elif media_notas >= (self.media_aprovacao * 0.75):
            return 'Regular'
        else:
            return 'Abaixo'

class Nota(models.Model):
    desempenho = models.ForeignKey(DesempenhoAluno, on_delete=models.CASCADE)
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    nota = models.FloatField()
    data = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.desempenho.aluno} - {self.materia} - {self.nota}'

