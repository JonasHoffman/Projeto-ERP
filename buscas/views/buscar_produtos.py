from django.http import JsonResponse
from buscas.services.produto_service import ProdutoService
from estoque.models import ProdutoBase

def buscar_produto(request):
    codigo = request.GET.get("q")
    contexto = request.GET.get("contexto")  # compra | venda | nfe | op

    if not codigo:
        return JsonResponse({"erro": "Código não informado"}, status=400)

    try:
        data = ProdutoService.buscar_por_codigo(codigo, contexto)
        return JsonResponse(data)

    except ProdutoBase.DoesNotExist:
        return JsonResponse({"erro": "Produto não encontrado"}, status=404)