from django.db import models
from estoque.models import Fornecedor,ProdutoBase
from decimal import Decimal
# Create your models here.
class PedidoCompra(models.Model):
    numero = models.CharField(max_length=20, unique=True, editable=False)
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.CASCADE)
    data_emissao = models.DateField(auto_now_add=True)
    valor_total = models.DecimalField(max_digits=12, decimal_places=2)
    valor_recebido = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(
        max_length=20,
        choices=[
            ('ABERTO', 'Aberto'),
            ('PARCIAL', 'Parcial'),
            ('CONCLUIDO', 'Concluído'),
        ],
        default='ABERTO'
    )
    

    def saldo_a_receber(self):
        return self.valor_total - self.valor_recebido
    
    
    valor_antecipado = models.DecimalField(
    max_digits=12,
    decimal_places=2,
    default=Decimal("0.00")
    )

    valor_recebido = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def atualizar_status(self):
        itens = self.itens.all()

        # Todos recebidos → concluído
        if all(item.quantidade_recebida >= item.quantidade for item in itens):
            self.status = "CONCLUIDO"

        # Algum recebido (mas não todos)
        elif any(item.quantidade_recebida > 0 for item in itens):
            self.status = "PARCIAL"

        else:
            self.status = "ABERTO"

        self.valor_recebido = sum([
            item.quantidade_recebida * item.valor_unitario
            for item in itens
        ])

        self.save()
        
    def save(self, *args, **kwargs):
        if not self.numero:
            ultimo = PedidoCompra.objects.order_by('-id').first()
            if ultimo:
                ultimo_numero = int(ultimo.numero.replace("PC-", ""))
                novo = ultimo_numero + 1
            else:
                novo = 1

            self.numero = f"PC-{novo:04d}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Pedido {self.numero}"

class PedidoCompraItem(models.Model):
    pedido = models.ForeignKey(PedidoCompra, on_delete=models.CASCADE, related_name="itens")
    produto = models.ForeignKey(ProdutoBase, on_delete=models.CASCADE)
    quantidade = models.DecimalField(max_digits=12, decimal_places=3)
    quantidade_recebida = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    valor_unitario = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['pedido', 'produto'],
                name='unique_produto_por_pedido'
            )
        ]

class PedidoCompraAntecipacao(models.Model):
    pedido = models.ForeignKey(PedidoCompra, on_delete=models.CASCADE, related_name="antecipacoes")
    data = models.DateField(auto_now_add=True)
    valor = models.DecimalField(max_digits=12, decimal_places=2)
    observacao = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Antecipação de R$ {self.valor} - Pedido {self.pedido.numero}"