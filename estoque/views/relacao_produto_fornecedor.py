from django.shortcuts import render, redirect
from django.contrib import messages
from estoque.forms import Relacionar_produto_FornecedorForm
import xmltodict
from estoque.models import Fornecedor, ProdutoFornecedor
from django.forms.formsets import formset_factory


def relacionar_produto(request):

    produtos_nao_encontrados = request.session.get('produtos_nao_encontrados', [])
    xml_temp = request.session.get('xml_temp')

    if not produtos_nao_encontrados or not isinstance(produtos_nao_encontrados, list):
        messages.error(request, 'Nenhum produto pendente para relacionar.')
        return redirect('estoque:receber_nfe')

    # Garante que cada item tem código e nome
    produtos_formatados = []
    for item in produtos_nao_encontrados:
        if isinstance(item, dict) and "codigo" in item and "nome" in item:
            produtos_formatados.append(item)

    if not produtos_formatados:
        messages.error(request, 'Nenhum produto válido para relacionar.')
        return redirect('estoque:receber_nfe')

    RelacionarFormSet = formset_factory(Relacionar_produto_FornecedorForm, extra=0)

    if request.method == 'POST':
        formset = RelacionarFormSet(request.POST)

        if formset.is_valid():
            xml_data = xmltodict.parse(xml_temp)
            cnpj = xml_data['nfeProc']['NFe']['infNFe']['emit']['CNPJ']

            fornecedor = Fornecedor.objects.filter(cnpj=cnpj).first()
            if not fornecedor:
                messages.error(request, 'Fornecedor não encontrado.')
                return redirect('estoque:receber_nfe')

            for form in formset:
                ProdutoFornecedor.objects.create(
                    fornecedor=fornecedor,
                    codigo_produto=form.cleaned_data['codigo'],
                    produto_estoque=form.cleaned_data['produto_estoque']
                )
            # Limpa sessão
            request.session.pop('produtos_nao_encontrados', None)

            messages.success(request, "Produtos relacionados com sucesso!")
            return redirect('estoque:receber_nfe')

    else:
        initial_data = [
            {
                'codigo': p['codigo'],
                'nome': p['nome']
            }
            for p in produtos_formatados
        ]

        formset = RelacionarFormSet(initial=initial_data)

    return render(request, 'recebimento/relacionar_produtos.html', {
        'formset': formset
    })
