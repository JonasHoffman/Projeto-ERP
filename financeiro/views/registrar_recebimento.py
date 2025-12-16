from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from datetime import datetime
from financeiro.models import ContaReceber, Recebimento
from django.core.paginator import Paginator
from datetime import date




def registrar_recebimentos(request):

    contas = ContaReceber.objects.all().order_by("vencimento")

    # FILTROS
    data_inicial = request.GET.get("data_inicial")
    data_final = request.GET.get("data_final")
    cliente = request.GET.get("cliente")
    situacao = request.GET.get("situacao")

    if data_inicial:
        contas = contas.filter(vencimento__gte=data_inicial)

    if data_final:
        contas = contas.filter(vencimento__lte=data_final)

    if cliente:
        contas = contas.filter(cliente__nome__icontains=cliente)

    if situacao and situacao != "":
        contas = contas.filter(situacao=situacao)

    # PROCESSAR BAIXA EM MASSA
    if request.method == "POST":

        selecionadas = request.POST.getlist("selecionadas")

        if not selecionadas:
            messages.warning(request, "Selecione ao menos uma conta.")
            return redirect("registrar_recebimentos")

        success = 0

        for conta_id in selecionadas:

            if not conta_id.isdigit():
                continue

            conta = get_object_or_404(ContaReceber, pk=conta_id)

            # ==============================
            # PEGAR DATA POR LINHA
            # ==============================
            data_key = f"data_recebimento_{conta_id}"
            data_str = request.POST.get(data_key)

            if data_str:
                try:
                    data_recebimento = datetime.strptime(data_str, "%Y-%m-%d").date()
                except ValueError:
                    data_recebimento = timezone.now().date()
            else:
                data_recebimento = timezone.now().date()

            # ==============================
            # PEGAR VALOR RECEBIDO POR LINHA
            # ==============================
            valor_key = f"valor_recebido_{conta_id}"
            valor_str = request.POST.get(valor_key)

            try:
                valor_recebido = float(valor_str) if valor_str else float(conta.saldo)
            except:
                valor_recebido = float(conta.saldo)

            if valor_recebido <= 0:
                continue

            # Criar o recebimento
            recibo = Recebimento.objects.create(
                conta=conta,
                valor_recebido=valor_recebido,
                forma_recebimento=conta.tipo_conta,
                usuario=request.user if request.user.is_authenticated else None,
                tipo_lancamento="NORMAL",
                observacao="Recebimento em massa.",
                data_recebimento=data_recebimento,
            )

            conta.atualizar_situacao()
            success += 1

        messages.success(request, f"{success} conta(s) baixadas com sucesso.")
        return redirect("registrar_recebimentos")

    # PAGINAÇÃO
    paginator = Paginator(contas, 20)  # 20 resultados por página
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)


    return render(request, "registrar_recebimentos.html", {
            "contas": page_obj,
            "filtros": {
                "data_inicial": data_inicial or "",
                "data_final": data_final or "",
                "cliente": cliente or "",
                "situacao": situacao or "",
            },
            "today": date.today(),   #  ⬅ ADICIONE ESTA LINHA
    })

from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from financeiro.models import Recebimento

from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from financeiro.models import Recebimento
from django.utils import timezone

def estornar_recebimento(request, recebimento_id):
    recebimento = get_object_or_404(Recebimento, id=recebimento_id)
    observacao = request.POST.get("observacao", "")

    # 1. Verificar se já existe estorno para este lançamento
    if Recebimento.objects.filter(estorna_de=recebimento).exists():
        messages.error(request, "Este recebimento já foi estornado anteriormente.")
        return redirect('registrar_recebimentos')
    print(observacao)
    # 2. Criar o lançamento de estorno
    Recebimento.objects.create(
        conta=recebimento.conta,
        valor_recebido = -recebimento.valor_recebido,
        forma_recebimento = recebimento.forma_recebimento,
        usuario = request.user if request.user.is_authenticated else None,
        tipo_lancamento = 'ESTORNO',
        observacao =  observacao,
        data_recebimento = timezone.now().date(),
        estorna_de = recebimento  # vínculo para impedir estorno duplo
    )

    messages.success(request, "Recebimento estornado com sucesso!")
    return redirect('registrar_recebimentos')
