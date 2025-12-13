from cadastros.forms import  ClienteForm,EnderecoFormSet,ContatoFormSet,DescontoClienteFormSet
from django.shortcuts import redirect,render


def cadastrar_cliente(request):
    if request.method == "POST":
        form = ClienteForm(request.POST)

        endereco_formset = EnderecoFormSet(request.POST)
        contato_formset = ContatoFormSet(request.POST)
        desconto_formset = DescontoClienteFormSet(request.POST)

        if (
            form.is_valid()
            and endereco_formset.is_valid()
            and contato_formset.is_valid()
            and desconto_formset.is_valid()
        ):
            cliente = form.save()

            endereco_formset.instance = cliente
            endereco_formset.save()

            contato_formset.instance = cliente
            contato_formset.save()

            desconto_formset.instance = cliente
            desconto_formset.save()

            return redirect("lista_clientes")

    else:
        form = ClienteForm()
        endereco_formset = EnderecoFormSet()
        contato_formset = ContatoFormSet()
        desconto_formset = DescontoClienteFormSet()

    return render(
        request,
        "cadastro_cliente.html",
        {
            "form": form,
            "endereco_formset": endereco_formset,
            "contato_formset": contato_formset,
            "desconto_formset": desconto_formset,
        }
    )
