from django.shortcuts import render, redirect
from cadastros.models import EnderecoFornecedor,ContatoFornecedor
from cadastros.forms import (
    FornecedorForm,
    EnderecoFormSet,
    ContatoFormSet
)
from django.utils.http import url_has_allowed_host_and_scheme

def cadastrar_fornecedor(request):
    next_url = request.GET.get('next') or request.POST.get('next')

    if request.method == "POST":
        form = FornecedorForm(request.POST)
        endereco_fs = EnderecoFormSet(request.POST, prefix="end")
        contato_fs = ContatoFormSet(request.POST, prefix="cont")

        if form.is_valid() and endereco_fs.is_valid() and contato_fs.is_valid():
            fornecedor = form.save()

            # Endereços
            enderecos = endereco_fs.save(commit=False)
            for e in enderecos:
                e.fornecedor = fornecedor
                e.save()

            # Contatos
            contatos = contato_fs.save(commit=False)
            for c in contatos:
                c.fornecedor = fornecedor
                c.save()

            # 🔁 REDIRECIONAMENTO INTELIGENTE
            if next_url and url_has_allowed_host_and_scheme(
                next_url,
                allowed_hosts={request.get_host()}
            ):
                return redirect(next_url)

            return redirect('cadastros:conta_list')

    else:
        form = FornecedorForm()
        endereco_fs = EnderecoFormSet(prefix="end")
        contato_fs = ContatoFormSet(prefix="cont")

    return render(request, 'cadastro_fornecedor.html', {
        'form': form,
        'endereco_fs': endereco_fs,
        'contato_fs': contato_fs,
        'next': next_url,
    })