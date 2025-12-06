from django.shortcuts import render
from cadastros.models import Cliente, Fornecedor, Transportadora, Banco
from django.db.models import Q

def buscar_clientes(request):
    termo = request.GET.get("q", "").strip()

    if termo:
        lista = Cliente.objects.filter(
            nome__icontains=termo
        ).order_by("nome")
    else:
        lista = Cliente.objects.all().order_by("nome")

    return render(request, "buscas/buscar_clientes.html", {"lista": lista})
