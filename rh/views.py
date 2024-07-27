import csv
from django.shortcuts import render
from .forms import ImportacaoPresencaForm
from .models import Presenca
import pandas as pd

def importar_presenca(request):
    if request.method == 'POST':
        form = ImportacaoPresencaForm(request.POST, request.FILES)
        if form.is_valid():
            arquivo = request.FILES['arquivo']
            df = pd.read_excel(arquivo)
            for _, linha in df.iterrows():
                Presenca.objects.create(
                    nome=linha['Nome'],
                    data=linha['Data'],
                    ausencia_dias=int(linha['Ausencia_dias']),
                    pedido_licenca_dias=int(linha['Pedido_licenca_dias']),
                    viagem_dias=int(linha['Viagem_dias']),
                    entrada_dias=int(linha['Entrada_dias']),
                    horas_extra=int(linha['Horas_extra']),
                    atraso=int(linha['Atraso']),
                    sair_cedo=int(linha['Sair_cedo']),
                )
            return render(request, 'importar_sucesso.html')
    else:
        form = ImportacaoPresencaForm()
    return render(request, 'importar_presenca.html', {'form': form})
