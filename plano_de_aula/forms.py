from django import forms
from .models import PlanoAula

class PlanoAulaForm(forms.ModelForm):
    class Meta:
        model = PlanoAula
        fields = ['titulo', 'descricao', 'arquivo']
