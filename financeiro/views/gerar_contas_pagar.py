from django.shortcuts import render, redirect
from financeiro.forms import ContasPagarForm

def criar_conta_pagar(request):
    if request.method == 'POST':
        form = ContasPagarForm(request.POST)
        if form.is_valid():
            conta = form.save(commit=False)
            conta.criado_por = request.user  # ⚙️ preenchido automaticamente
            conta.save()
            print('nada')
            return redirect('registrar_pagamentos')  # ajuste para sua rota
        else:
            print(form.errors)
    else:
        form = ContasPagarForm()
    return render(request, 'contas_pagar.html', {'form': form})
