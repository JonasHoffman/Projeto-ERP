from decimal import Decimal
from cadastros.models import RegraPreco

class PriceService:

    @staticmethod
    def calcular(produto, cliente):
        preco = produto.preco_venda  # PREÇO BASE

        regras = RegraPreco.objects.filter(
            ativo=True,
            tabela_preco=cliente.tabela_preco
        )

        regra_escolhida = None
        maior_nivel = -1

        for regra in regras:
            if not PriceService._aplica(regra, cliente):
                continue

            nivel = regra.nivel_especificidade()

            if nivel > maior_nivel:
                maior_nivel = nivel
                regra_escolhida = regra

        if regra_escolhida:
            preco += preco * (regra_escolhida.percentual / Decimal('100'))

        return preco

    @staticmethod
    def _aplica(regra, cliente):
        # Estado
        if regra.estado:
            if not cliente.endereco:
                return False
            if regra.estado != cliente.endereco.estado:
                return False

        # Tipo de cliente
        if regra.tipo_cliente and regra.tipo_cliente != cliente.tipo_cliente:
            return False

        return True
