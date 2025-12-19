# produtos/views.py
from django.shortcuts import render, redirect, get_object_or_404
from cadastros.models import ProdutoBase
from cadastros.forms import ProdutoBaseForm




def listar_produtos_base(request):
    produtos = ProdutoBase.objects.all()
    return render(
    request,
    "cadastro_produtobase.html",
    {"produtos": produtos}
    )




def cadastrar_produto_base(request):
    form = ProdutoBaseForm()
    if request.method == "POST":
        form = ProdutoBaseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("listar_produtos_base")
        else:
            form = ProdutoBaseForm()


    return render(
    request,
    "cadastro_produtobase_form.html",
    {"form": form, "titulo": "Cadastrar Produto"}
    )




def editar_produto_base(request, pk):
    produto = get_object_or_404(ProdutoBase, pk=pk)


    if request.method == "POST":
        form = ProdutoBaseForm(request.POST, instance=produto)
        if form.is_valid():
            form.save()
            return redirect("listar_produtos_base")
        else:
            form = ProdutoBaseForm(instance=produto)


    return render(
    request,
    "cadastro_produto_base_form.html",
    {"form": form, "titulo": "Editar Produto"}
    )