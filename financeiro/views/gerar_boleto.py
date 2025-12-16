from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import date, timedelta
from financeiro.models import ContaReceber
from vendas.models import Pedido
from credenciais_efi import EFIPAY_CREDENTIALS
from efipay import EfiPay
import json
import re


# ===============================
# Função valida telefone EFÍ
# ===============================
def validar_telefone(numero):
    numero = re.sub(r"\D", "", numero or "")
    if re.fullmatch(r"^[1-9]{2}9?[0-9]{8}$", numero):
        return numero
    return None


# ===============================
# Gerar boleto real para um pedido
# ===============================
def gerar_boleto(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)

    telefone = validar_telefone(pedido.cliente.telefone)
    if not telefone:
        return JsonResponse({"erro": "Telefone inválido (padrão EFÍ)"}, status=400)

    efi = EfiPay(EFIPAY_CREDENTIALS)

    body = {
        "items": [
            {"name": f"Pedido {pedido.numero}", "value": int(pedido.valor * 100), "amount": 1}
        ],
        "payment": {
            "banking_billet": {
                "expire_at": (date.today() + timedelta(days=5)).isoformat(),
                "customer": {
                    "name": str(pedido.cliente),
                    "cpf": pedido.cliente.cpf,
                    "email": pedido.cliente.email,
                    "phone_number": telefone,
                },
                "message": f"Pagamento referente ao Pedido {pedido.numero}"
            }
        },
        "metadata": {
            "notification_url": "http://localhost:8000/webhook/efi/"
        }
    }

    try:
        resp = efi.create_one_step_charge(body=body)
    except Exception as e:
        return JsonResponse({"erro": "Falha ao gerar boleto", "detalhe": str(e)}, status=400)

    charge_id = resp["data"]["charge_id"]
    boleto_url = resp["data"]["billet_link"]

    ContaReceber.objects.create(
        pedido=pedido,
        cliente=pedido.cliente,
        tipo_conta="Boleto",
        valor_total=pedido.valor,
        vencimento=date.today() + timedelta(days=5),
        boleto_url=boleto_url,
        charge_id=charge_id,
        situacao="Aberta",
        criado_por=request.user,
    )

    return redirect("contas_receber")


# ===============================
# Listar contas a receber
# ===============================
def contas_receber(request):
    contas = ContaReceber.objects.all()
    return render(request, "contas_receber.html", {"contas": contas})


# ===============================
# Webhook de atualização de status
# ===============================
@csrf_exempt
def webhook_efi(request):
    try:
        evento = json.loads(request.body.decode())
    except:
        return JsonResponse({"erro": "JSON inválido"}, status=400)

    charge_id = evento.get("charge_id")
    status = evento.get("status")  # waiting, paid, canceled

    if not charge_id:
        return JsonResponse({"erro": "sem charge_id"}, status=400)

    conta = ContaReceber.objects.filter(charge_id=charge_id).first()
    if not conta:
        return JsonResponse({"erro": "conta não encontrada"}, status=404)

    if status == "paid":
        conta.situacao = "Recebida"
        conta.save(update_fields=["situacao"])

    elif status == "canceled":
        conta.situacao = "Cancelada"
        conta.save(update_fields=["situacao"])

    return JsonResponse({"ok": True})


# ===============================
# Gerar boleto de teste
# ===============================
def gerar_boleto_teste(request):
    efi = EfiPay(EFIPAY_CREDENTIALS)

    telefone = validar_telefone("51999999999")
    if not telefone:
        return JsonResponse({"erro": "Telefone inválido"}, status=400)

    body = {
        "items": [
            {"name": "Boleto Teste", "value": 1000, "amount": 1}
        ],
        "payment": {
            "banking_billet": {
                "expire_at": (date.today() + timedelta(days=3)).isoformat(),
                "customer": {
                    "name": "Usuário Teste",
                    "cpf": "12345678909",
                    "email": "teste@teste.com",
                    "phone_number": telefone
                },
                "message": "Boleto de teste"
            }
        }
    }

    try:
        resp = efi.create_one_step_charge(body=body)
    except Exception as e:
        return JsonResponse({"erro": "Falha ao gerar boleto teste", "detalhe": str(e)}, status=400)

    return JsonResponse({
        "charge_id": resp["data"]["charge_id"],
        "boleto_url": resp["data"]["billet_link"]
    })
