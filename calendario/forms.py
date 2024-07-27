from django import forms
from .models import Evento, Users

class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ['titulo', 'descricao', 'tipo', 'data_inicio', 'data_fim', 'usuarios_destinados']
        widgets = {
            'data_inicio': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'data_fim': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'usuarios_destinados': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }
