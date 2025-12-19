# cadastros/views.py
from django.shortcuts import render, redirect, get_object_or_404
from cadastros.models import GrupoProduto
from cadastros.forms import GrupoProdutoForm

def grupo_produto_listar(request):
    grupos = GrupoProduto.objects.all().order_by('codigo')
    return render(request, 'cadastro_grupo.html', {
        'grupos': grupos
    })


def grupo_produto_criar(request):
    if request.method == 'POST':
        form = GrupoProdutoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cadastros:grupo_produto_listar')
    else:
        form = GrupoProdutoForm()

    return render(request, 'cadastro_grupo_form.html', {
        'form': form,
        'titulo': 'Cadastrar Grupo de Produto'
    })

def grupo_produto_editar(request, pk):
    grupo = get_object_or_404(GrupoProduto, pk=pk)

    if request.method == 'POST':
        form = GrupoProdutoForm(request.POST, instance=grupo)
        if form.is_valid():
            form.save()
            return redirect('cadastros:grupo_produto_listar')
    else:
        form = GrupoProdutoForm(instance=grupo)

    return render(request, 'cadastro_grupo_form.html', {
        'form': form,
        'titulo': 'Editar Grupo de Produto'
    })