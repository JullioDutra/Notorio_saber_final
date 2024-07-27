# forms.py
from django import forms

class ImportacaoPresencaForm(forms.Form):
    arquivo = forms.FileField()
