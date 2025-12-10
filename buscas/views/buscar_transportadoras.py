from django.shortcuts import render
from cadastros.models import Transportadora

def buscar_transportadoras(request):
    termo = request.GET.get("q", "").strip()

    if termo:
        lista = Transportadora.objects.filter(
            nome__icontains=termo
        ).order_by("nome")
    else:
        # ➜ Sem termo → retorna tudo
        lista = Transportadora.objects.all().order_by("nome")

    return render(request, "buscas/buscar_transportadoras.html", {
    "transportadoras": lista,
    "query": termo
})