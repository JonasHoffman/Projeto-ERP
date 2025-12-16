from django.shortcuts import render, get_object_or_404, redirect
# from django.contrib import messages
# from financeiro.models import ContasPagar, Pagamento
# from django.contrib.auth.decorators import login_required
# from decimal import Decimal



# def registrar_pagamento(request, conta_id):
#     conta = get_object_or_404(ContasPagar, pk=conta_id)

#     if request.method == 'POST':
#         valor = Decimal(request.POST.get('valor_pago'))
#         forma = request.POST.get('forma_pagamento')
#         observacao = request.POST.get('observacao', '')

#         Pagamento.objects.create(
#             conta=conta,
#             valor_pago=valor,
#             forma_pagamento=forma,
#             usuario=request.user,
#             tipo_lancamento='NORMAL',
#             observacao=observacao
#         )
#         conta.atualizar_situacao()
#         messages.success(request, "Pagamento registrado com sucesso.")
#         return redirect('registrar_pagamento',conta_id=conta.pk)

#     return render(request, 'registra_pagamento.html', {'conta': conta})


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from decimal import Decimal
from datetime import datetime
from financeiro.models import ContasPagar, Pagamento
from cadastros.models import FormaPagamento


def registrar_pagamentos(request):
    contas = ContasPagar.objects.exclude(situacao='Paga').order_by('dt_vencimento')
    # --- FILTROS ---
    data_inicial = request.GET.get('data_inicial')
    data_final = request.GET.get('data_final')
    fornecedor = request.GET.get('fornecedor')

    if data_inicial:
        contas = contas.filter(dt_vencimento__gte=data_inicial)
    if data_final:
        contas = contas.filter(dt_vencimento__lte=data_final)
    if fornecedor:
        contas = contas.filter(cod_cliente__nome__icontains=fornecedor)

    # --- FORMAS DE PAGAMENTO ---
    formas_pagamento = [
        ('DINHEIRO', 'Dinheiro'),
        ('PIX', 'PIX'),
        ('BOLETO', 'Boleto'),
        ('TRANSFERENCIA', 'Transferência'),
        ('CARTAO', 'Cartão'),
    ]
    formas_pagamento = FormaPagamento.objects.all()
    # --- PROCESSAR PAGAMENTOS ---
    if request.method == 'POST':
        print('create')
        data_padrao = request.POST.get('data_padrao')
        forma_padrao = request.POST.get('forma_padrao')
        selecionadas = request.POST.getlist('selecionadas')
        print(selecionadas)
        # 🧩 1. Verificação de seleção
        if not selecionadas:
            messages.warning(request, "Selecione pelo menos uma conta para baixar.")
            return redirect('registrar_pagamentos')

        # 🧩 2. Loop nas contas selecionadas
        for conta_id in selecionadas:
            print('create1')
            # garante que o ID é válido
            if not conta_id.isdigit():
                continue
            
            conta = get_object_or_404(ContasPagar, pk=conta_id)
            print('create3')
            valor_str = request.POST.get(f'valor_pago_{conta_id}') or conta.saldo
            data_pg = request.POST.get(f'data_pg_{conta_id}') or data_padrao
            forma_id = request.POST.get(f'forma_{conta_id}') or forma_padrao

            forma_pagamento = None
            if forma_id:
                forma_pagamento = FormaPagamento.objects.get(pk=forma_id)
            # 🧩 3. Verificação de valor válido
            
            if not valor_str:
                continue

            try:
                valor = Decimal(valor_str)
            except:
                continue

            if valor <= 0:
                continue

            data_pagamento = datetime.strptime(data_pg, '%Y-%m-%d') if data_pg else datetime.now()

            # Cria o pagamento
            Pagamento.objects.create(
                conta=conta,
                valor_pago=valor,
                forma_pagamento=forma_pagamento,
                usuario=request.user,
                tipo_lancamento='NORMAL',
                data_pagamento=data_pagamento,
            )

            conta.atualizar_situacao()

        messages.success(request, f"{len(selecionadas)} pagamento(s) registrado(s) com sucesso.")
        return redirect('registrar_pagamentos')

    # --- RENDER TEMPLATE ---
    return render(request, 'registrar_pagamentos.html', {
        'contas': contas,
        'formas_pagamento': formas_pagamento,
        'filtros': {
            'data_inicial': data_inicial or '',
            'data_final': data_final or '',
            'fornecedor': fornecedor or '',
        },
    })


def estornar_pagamento(request, pagamento_id):
    pagamento = get_object_or_404(
        Pagamento,
        pk=pagamento_id,
        tipo_lancamento='NORMAL'
    )
    conta = pagamento.conta

    # 🚫 já estornado?
    if hasattr(pagamento, 'estorno'):
        messages.error(
            request,
            f"O pagamento {pagamento.pk} já foi estornado."
        )
        return redirect('fluxo_caixa')

    # ✅ cria estorno vinculado
    Pagamento.objects.create(
        conta=conta,
        valor_pago=-pagamento.valor_pago,
        forma_pagamento=pagamento.forma_pagamento,
        usuario=request.user,
        tipo_lancamento='ESTORNO',
        pagamento_origem=pagamento,
        observacao=f"Estorno do pagamento ID {pagamento.pk}"
    )

    conta.atualizar_situacao()

    messages.warning(
        request,
        f"Pagamento {pagamento.pk} estornado com sucesso."
    )

    return redirect('fluxo_caixa')
