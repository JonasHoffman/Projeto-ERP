# cadastros/views/transportadora.py

from django.shortcuts import render, redirect, get_object_or_404
from cadastros.models import Transportadora
from cadastros.forms import TransportadoraForm
from django.http import HttpResponse

def transportadora_list(request):
    transportadoras = Transportadora.objects.all().order_by('nome')
    return render(request, 'cadastro_transportadora.html', {
        'transportadoras': transportadoras
    })


def transportadora_create(request):
    if request.method == 'POST':
        form = TransportadoraForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cadastros:transportadora_list')
    else:
        form = TransportadoraForm()

    return render(request, 'cadastro_transportadora_form.html', {
        'form': form,
        'titulo': 'Cadastrar Transportadora'
    })


def transportadora_update(request, pk):
    transportadora = get_object_or_404(Transportadora, pk=pk)

    if request.method == 'POST':
        form = TransportadoraForm(request.POST, instance=transportadora)
        if form.is_valid():
            form.save()
            return redirect('cadastros:transportadora_list')
    else:
        form = TransportadoraForm(instance=transportadora)

    return render(request, 'cadastro_transportadora_form.html', {
        'form': form,
        'titulo': 'Editar Transportadora'
    })
