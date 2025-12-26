from decimal import Decimal
from datetime import date, timedelta
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from compras.models import PedidoCompra,PedidoCompraItem
from estoque.models import (
    ProdutoEntradaTemp, ProdutoEntrada, Deposito, MovEstoque,
    NotaFiscalEntrada
)
from estoque.forms import recebimento_em_estoqueForm
from financeiro.models import ContasPagar   # <-- IMPORTANTE


@csrf_exempt
def recebimento_nf_interna(request, numero_nf):

    itens_nf = ProdutoEntradaTemp.objects.filter(finalizado=False, numero_nf=numero_nf)
    depositos = Deposito.objects.all()
    form_nf = recebimento_em_estoqueForm()

    # -------------------------------------------------------------------
    # GET — Renderizar tela de recebimento
    # -------------------------------------------------------------------
    if request.method == "GET":

        pedido_auto = None

        if itens_nf.exists():

            fornecedor = itens_nf.first().fornecedor
            produtos_nf = itens_nf.values_list('produto_id', flat=True)

            pedidos = PedidoCompra.objects.filter(
                fornecedor=fornecedor,
                status__in=["ABERTO", "PARCIAL"]
            )

            for pedido in pedidos:
                itens_pedido = PedidoCompraItem.objects.filter(
                    pedido=pedido
                ).values_list('produto_id', flat=True)

                if any(p in itens_pedido for p in produtos_nf):
                    pedido_auto = pedido
                    break

        return render(request, "recebimento/recebimento_nf_interna.html", {
            'nf': itens_nf,
            'depositos': depositos,
            'numero_nf': numero_nf,
            'form': form_nf,
            'nomes_itens': list(itens_nf.values_list('produto__nome', flat=True)),
            'pedido_encontrado': pedido_auto,
        })

    # -------------------------------------------------------------------
    # POST — Processamento da NF
    # -------------------------------------------------------------------
    if not itens_nf.exists():
        return JsonResponse({'erro': 'NF não encontrada ou já finalizada'}, status=400)

    # PRIMEIRA MANEIRA — JSON no body
    try:
        data = json.loads(request.body)
    except:
        return JsonResponse({'erro': 'JSON inválido enviado.'}, status=400)

    print("POST RECEBIDO:", data)

    # Agora vem o número do pedido, não o ID
    pedido_numero = data.get("pedido_numero")

    if not pedido_numero:
        return JsonResponse({'erro': 'Pedido de compra é obrigatório.'}, status=400)

    # BUSCA pelo campo numero (ex.: "PC-0118")
    pedido = PedidoCompra.objects.filter(numero=pedido_numero).first()

    if not pedido:
        return JsonResponse({'erro': f"Pedido '{pedido_numero}' não encontrado."}, status=400)

    fornecedor = itens_nf.first().fornecedor

    nf_registro = NotaFiscalEntrada.objects.filter(
        numero=numero_nf,
        fornecedor=fornecedor
    ).first()

    if not nf_registro:
        return JsonResponse({'erro': 'NF não cadastrada no sistema'}, status=400)

    # Depósito
    deposito_id = data.get("deposito")
    deposito = Deposito.objects.filter(id=deposito_id).first() or Deposito.objects.first()

    lote_digitado = data.get("lote", "")
    valor_total_nf = nf_registro.valor_total

    # -------------------------------------------------------------------
    # SALVAR ITENS
    # -------------------------------------------------------------------
    for item in itens_nf:

        produto = item.produto

        item_pedido = PedidoCompraItem.objects.filter(
            pedido=pedido,
            produto=produto
        ).first()

        # Movimentação
        MovEstoque.objects.create(
            produto=produto,
            lote=lote_digitado,
            deposito=deposito,
            tipo='ENTRADA',
            quantidade=item.quantidade,
            motivo=f"Entrada NF {numero_nf}",
            usuario=request.user
        )

        # ProdutoEntrada (definitivo)
        ProdutoEntrada.objects.create(
            produto=produto,
            fornecedor=fornecedor,
            fornecedor_nome=fornecedor.nome_fantasia,
            quantidade=item.quantidade,
            custo_unitario=item.custo_unitario,
            custo_total=item.custo_total,
            lote=lote_digitado,
            deposito=deposito
        )

        # Atualiza item do pedido
        if item_pedido:
            item_pedido.quantidade_recebida += Decimal(item.quantidade)
            item_pedido.save()

    # -------------------------------------------------------------------
    # Atualizar PedidoCompra
    # -------------------------------------------------------------------
    pedido.valor_recebido += Decimal(valor_total_nf)

    if pedido.valor_recebido >= pedido.valor_total:
        pedido.status = "CONCLUIDO"
    elif pedido.valor_recebido > 0:
        pedido.status = "PARCIAL"
    else:
        pedido.status = "ABERTO"

    pedido.save()

    # -------------------------------------------------------------------
    # Criar Contas a Pagar
    # -------------------------------------------------------------------
    data_emissao_nf = nf_registro.data_emissao or date.today()
    data_vencimento = data_emissao_nf + timedelta(days=30)

    conta = ContasPagar.objects.create(
        cod_cliente=fornecedor,
        cod_banco=None,
        forma_pagamento=None,
        tipo_conta='Fatura',
        situacao='Aberta',
        dt_vencimento=data_vencimento,
        total_titulo=valor_total_nf,
        multa=Decimal('0.00'),
        criado_por=request.user
    )

    print("Contas a Pagar criada:", conta.titulo)

    # -------------------------------------------------------------------
    # Finalização
    # -------------------------------------------------------------------
    return JsonResponse({
        "ok": True,
        "mensagem": "NF recebida com sucesso!",
        "contas_pagar_id": conta.titulo
    })
