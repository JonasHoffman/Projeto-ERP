from django.shortcuts import render, redirect, get_object_or_404
from cadastros.models import Banco, ContaFinanceira
from cadastros.forms import BancoForm, ContaFinanceiraForm
# =========================
# CONTA FINANCEIRA
# =========================

def conta_list(request):
    contas = ContaFinanceira.objects.select_related('banco').order_by('descricao')
    return render(request, 'cadastro_conta_financeira.html', {
        'contas': contas
    })


def conta_create(request):
    if request.method == 'POST':
        form = ContaFinanceiraForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cadastros:conta_list')
    else:
        form = ContaFinanceiraForm()

    return render(request, 'cadastro_conta_financeira_form.html', {
        'form': form,
        'titulo': 'Nova Conta Financeira'
    })


def conta_update(request, pk):
    conta = get_object_or_404(ContaFinanceira, pk=pk)

    if request.method == 'POST':
        form = ContaFinanceiraForm(request.POST, instance=conta)
        if form.is_valid():
            form.save()
            return redirect('cadastros:conta_list')
    else:
        form = ContaFinanceiraForm(instance=conta)

    return render(request, 'cadastro_conta_financeira_form.html', {
        'form': form,
        'titulo': 'Editar Conta Financeira'
    })
