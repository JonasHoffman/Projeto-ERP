from estoque.models import ProdutoBase

class ProdutoService:

    @staticmethod
    def buscar_por_codigo(codigo, contexto=None):
        produto = ProdutoBase.objects.select_related("unidade").get(
            codigo__iexact=codigo.strip()
        )

        data = {
            "id": produto.id,
            "codigo": produto.codigo,   # ← mantém o código real
            "nome": produto.nome,
            "unidade": produto.unidade.sigla if produto.unidade else "",
        }

        if contexto == "compra":
            data["preco"] = float(produto.preco_base or 0)

        elif contexto == "venda":
            data["preco"] = float(produto.preco_venda or 0)
            data["estoque"] = produto.estoque_atual()

        elif contexto == "nfe":
            data["ncm"] = produto.ncm

        return data
