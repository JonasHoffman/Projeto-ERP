from django.shortcuts import render, redirect, get_object_or_404
from compras.models import PedidoCompra, PedidoCompraItem,PedidoCompraAntecipacao
from compras.forms import PedidoCompraForm,PedidoItemFormSet,PedidoCompraAntecipacaoForm
from decimal import Decimal
from django.db.models import Sum


# ======================================================
# LISTAR PEDIDOS
# ======================================================
def compras_em_aberto(request):
    pedidos = PedidoCompra.objects.all().order_by('-id')
    return render(request, 'compras/lista_compras_em_aberto.html', {'pedidos': pedidos})


# ======================================================
# CRIAR PEDIDO
# ======================================================



def compras_criar_pedido(request):
    pedido = PedidoCompra()

    if request.method == "POST":
        form = PedidoCompraForm(request.POST)
        formset = PedidoItemFormSet(request.POST, instance=pedido)

        if form.is_valid() and formset.is_valid():
            pedido = form.save(commit=False)

            # total baseado nos itens
            pedido.valor_total = 0

            pedido.save()
            formset.instance = pedido
            itens = formset.save()

            # recalcula total
            total = sum(i.quantidade * i.valor_unitario for i in itens)
            pedido.valor_total = total
            pedido.save(update_fields=['valor_total'])

            return redirect("compras:compras_detalhe_pedido", pedido.id)

    else:
        form = PedidoCompraForm()
        formset = PedidoItemFormSet(instance=pedido)

    return render(request, 'compras/compras_criar_pedido.html', {
        "form": form,
        "formset": formset
    })


# ======================================================
# DETALHAR PEDIDO

def compras_detalhe_pedido(request, pedido_id):
    pedido = get_object_or_404(PedidoCompra, id=pedido_id)

    total_antecipado = pedido.antecipacoes.aggregate(
        total=Sum("valor")
    )["total"] or 0

    # 🔴 ESSENCIAL
    formset = PedidoItemFormSet(
        instance=pedido,
        queryset=pedido.itens.all()
    )

    return render(request, "compras/compras_detalhe_pedido.html", {
        "pedido": pedido,
        "itens": pedido.itens.all(),
        "antecipacoes": pedido.antecipacoes.all(),
        "total_antecipado": total_antecipado,
        "formset": formset,  # 🔴 AGORA EXISTE
    })



# ======================================================
# EDITAR PEDIDO
# ======================================================
def compras_editar_pedido(request, pedido_id):
    pedido = get_object_or_404(PedidoCompra, id=pedido_id)

    if request.method == 'POST':
        form = PedidoCompraForm(request.POST, instance=pedido)
        if form.is_valid():
            form.save()
            return redirect('compras:detalhe_pedido', pedido_id=pedido.id)
    else:
        form = PedidoCompraForm(instance=pedido)

    return render(request, 'estoque/compras/pedido_detalhe.html', {'form': form, 'titulo': "Editar Pedido"})


# ======================================================
# ADICIONAR ITEM AO PEDIDO
# ======================================================
def compras_adicionar_item(request, pedido_id):
    pedido = get_object_or_404(PedidoCompra, id=pedido_id)

    if request.method == 'POST':
        formset = PedidoItemFormSet(request.POST, instance=pedido)

        if formset.is_valid():
            itens = formset.save(commit=False)

            for item in itens:
                item.quantidade_recebida = 0
                item.save()

            return redirect(
                'compras:compras_detalhe_pedido',
                pedido_id=pedido.id
            )

    return redirect(
        'compras:compras_detalhe_pedido',
        pedido_id=pedido.id
    )


# ======================================================
# REMOVER ITEM
# ======================================================
def compras_remover_item(request, pedido_id, item_id):
    pedido = get_object_or_404(PedidoCompra, id=pedido_id)

    item = get_object_or_404(
        PedidoCompraItem,
        id=item_id,
        pedido=pedido  # 🔴 garante que pertence ao pedido
    )

    item.delete()

    return redirect(
        "compras:compras_detalhe_pedido",
        pedido_id=pedido.id
    )



def compras_adicionar_antecipacao(request, pedido_id):
    pedido = get_object_or_404(PedidoCompra, id=pedido_id)
    if request.method == "POST":
        valor = request.POST.get("valor")
        observacao = request.POST.get("observacao", "")
        if valor:
            PedidoCompraAntecipacao.objects.create(
                pedido=pedido,
                valor=valor,
                observacao=observacao
            )
    return redirect('compras:compras_detalhe_pedido', pedido_id=pedido.id)
