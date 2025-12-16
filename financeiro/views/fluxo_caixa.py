from django.shortcuts import render
from datetime import datetime
from financeiro.models import Pagamento, Recebimento


def fluxo_caixa(request):
    data_inicio = request.GET.get("data_inicio")
    data_fim = request.GET.get("data_fim")

    try:
        data_inicio = datetime.strptime(data_inicio, "%Y-%m-%d").date() if data_inicio else None
    except:
        data_inicio = None

    try:
        data_fim = datetime.strptime(data_fim, "%Y-%m-%d").date() if data_fim else None
    except:
        data_fim = None

    lancamentos = []

    # ---------------------------
    # RECEBIMENTOS (ENTRADA)
    # ---------------------------
    recebimentos = Recebimento.objects.all()

    if data_inicio:
        recebimentos = recebimentos.filter(data_recebimento__gte=data_inicio)
    if data_fim:
        recebimentos = recebimentos.filter(data_recebimento__lte=data_fim)

    for r in recebimentos:
        lancamentos.append({
            "data": r.data_recebimento,
            "descricao": f"Recebimento #{r.id} - Cliente: {r.conta.cliente.nome if r.conta and r.conta.cliente else ''}",
            "valor": r.valor_recebido,
            "tipo": "Entrada",
            "pagamento": None,  # não existe estorno aqui
        })

    # ------------------------
    # PAGAMENTOS (SAÍDA)
    # ------------------------
    pagamentos = Pagamento.objects.select_related(
        "conta", "forma_pagamento", "usuario"
    )

    if data_inicio:
        pagamentos = pagamentos.filter(data_pagamento__gte=data_inicio)
    if data_fim:
        pagamentos = pagamentos.filter(data_pagamento__lte=data_fim)

    for p in pagamentos:
        lancamentos.append({
            "data": p.data_pagamento,
            "descricao": f"Pagamento #{p.id} - Fornecedor: {p.conta.cod_cliente.nome_fantasia if p.conta and p.conta.cod_cliente else ''}",
            "valor": p.valor_pago,
            "tipo": "Saída",
            "pagamento": p,  # 🔥 AQUI ESTÁ A CHAVE
        })

    # -------------------------
    # ORDENAÇÃO
    # -------------------------
    lancamentos.sort(key=lambda x: x["data"])

    total_entradas = sum(l["valor"] for l in lancamentos if l["tipo"] == "Entrada")
    total_saidas = sum(l["valor"] for l in lancamentos if l["tipo"] == "Saída")
    saldo_final = total_entradas - total_saidas

    return render(request, "fluxo_caixa.html", {
        "lancamentos": lancamentos,
        "total_entradas": total_entradas,
        "total_saidas": total_saidas,
        "saldo_final": saldo_final,
        "data_inicio": data_inicio,
        "data_fim": data_fim,
    })
