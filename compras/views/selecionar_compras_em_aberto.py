# estoque/views.py

from django.shortcuts import render
from compras.models import PedidoCompra

def selecionar_compras_em_aberto(request):
    pedidos = PedidoCompra.objects.filter(status="ABERTO")
    return render(request, "compras/selecionar_compras_em_aberto.html", {
        "pedidos": pedidos
    })
