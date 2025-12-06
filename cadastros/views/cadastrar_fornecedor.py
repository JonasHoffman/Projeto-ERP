from django.shortcuts import render, redirect
from cadastros.models import EnderecoFornecedor,ContatoFornecedor
from cadastros.forms import (
    FornecedorForm,
    EnderecoFormSet,
    ContatoFormSet
)

def cadastrar_fornecedor(request):
    if request.method == "POST":
        form = FornecedorForm(request.POST)
        endereco_fs = EnderecoFormSet(request.POST, prefix="end")
        contato_fs = ContatoFormSet(request.POST, prefix="cont")

        if form.is_valid() and endereco_fs.is_valid() and contato_fs.is_valid():
            fornecedor = form.save()

            # 🔹 Salva endereços
            enderecos = endereco_fs.save(commit=False)
            for e in enderecos:
                e.fornecedor = fornecedor
                e.save()

            # 🔹 Salva contatos
            contatos = contato_fs.save(commit=False)
            for c in contatos:
                c.fornecedor = fornecedor
                c.save()

            return redirect("lista_fornecedores")

    else:
        form = FornecedorForm()
        endereco_fs = EnderecoFormSet(prefix="end", queryset=EnderecoFornecedor.objects.none())
        contato_fs = ContatoFormSet(prefix="cont", queryset=ContatoFornecedor.objects.none())

    return render(request, "cadastro_fornecedor.html", {
        "form": form,
        "endereco_fs": endereco_fs,
        "contato_fs": contato_fs,
    })
