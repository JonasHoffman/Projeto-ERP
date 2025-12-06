from cadastros.models import Banco
from django.shortcuts import render

def buscar_bancos(request):
    termo = request.GET.get("q", "").strip()

    if termo:
        lista = Banco.objects.filter(
            nome__icontains=termo
        ).order_by("nome")
    else:
        lista = Banco.objects.all().order_by("nome")

    return render(request, "buscas/buscar_bancos.html", {"lista": lista})
