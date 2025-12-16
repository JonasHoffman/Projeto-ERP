# cadastros/views_financeiro.py (ou no views.py)

from django.shortcuts import render, redirect, get_object_or_404
from cadastros.models import Banco, ContaFinanceira
from cadastros.forms import BancoForm, ContaFinanceiraForm


# =========================
# BANCO
# =========================

def banco_list(request):
    bancos = Banco.objects.all().order_by('nome')
    return render(request, 'cadastro_banco.html', {
        'bancos': bancos
    })


def banco_create(request):
    if request.method == 'POST':
        form = BancoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cadastros:banco_list')
    else:
        form = BancoForm()

    return render(request, 'cadastro_banco_form.html', {
        'form': form,
        'titulo': 'Novo Banco'
    })


def banco_update(request, pk):
    banco = get_object_or_404(Banco, pk=pk)

    if request.method == 'POST':
        form = BancoForm(request.POST, instance=banco)
        if form.is_valid():
            form.save()
            return redirect('cadastros:banco_list')
    else:
        form = BancoForm(instance=banco)

    return render(request, 'cadastro_banco_form.html', {
        'form': form,
        'titulo': 'Editar Banco'
    })
