from django.contrib import admin
from .models import Materia, DesempenhoAluno, Nota

@admin.register(Materia)
class MateriaAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)

@admin.register(DesempenhoAluno)
class DesempenhoAlunoAdmin(admin.ModelAdmin):
    list_display = ('aluno', 'media_aprovacao')
    search_fields = ('aluno__username', 'aluno__first_name', 'aluno__last_name')

@admin.register(Nota)
class NotaAdmin(admin.ModelAdmin):
    list_display = ('desempenho', 'materia', 'nota', 'data')
    search_fields = ('desempenho__aluno__username', 'materia__nome')
    list_filter = ('materia', 'data')
