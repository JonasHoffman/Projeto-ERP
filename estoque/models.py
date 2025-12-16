from django.db import models
from django.contrib.auth.models import User
from django.apps import apps


# Create your models here.
class ProdutoEntradaTemp(models.Model):
    produto = models.ForeignKey('cadastros.ProdutoBase', on_delete=models.CASCADE)
    fornecedor = models.ForeignKey('cadastros.Fornecedor', on_delete=models.CASCADE)
    quantidade = models.FloatField()
    custo_unitario = models.DecimalField(max_digits=10, decimal_places=4)
    custo_total = models.DecimalField(max_digits=12, decimal_places=4)
    numero_nf = models.CharField(max_length=20)
    finalizado = models.BooleanField(default=False)
    recebido = models.ForeignKey(User,on_delete=models.SET_NULL,blank=True,null=True)
    def save(self,*args,**kwargs):
        if not self.recebido:
            recebido = self.user
        super().save(*args,**kwargs)

class MovEstoque(models.Model):
    TIPO = [
        ('ENTRADA', 'Entrada'),
        ('SAIDA', 'Saída'),
        ('ACERTO_POSITIVO', 'Acerto (+)'),
        ('ACERTO_NEGATIVO', 'Acerto (-)'),
    ]

    produto = models.ForeignKey('cadastros.ProdutoBase', on_delete=models.CASCADE)
    lote = models.CharField(max_length=25, null=True, blank=True)  # opcional
    deposito = models.ForeignKey('cadastros.Deposito', on_delete=models.SET_NULL, null=True, blank=True)
    tipo = models.CharField(max_length=20, choices=TIPO)
    quantidade = models.DecimalField(max_digits=10, decimal_places=2)
    motivo = models.CharField(max_length=255, null=True, blank=True)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    data = models.DateTimeField(auto_now_add=True)

class ProdutoFornecedor(models.Model):
    cnpj_fornecedor = models.ForeignKey('cadastros.Fornecedor',on_delete=models.SET_NULL,blank=True,null=True)
    nome_produto = models.CharField(max_length=50) 
    codigo_produto = models.CharField(max_length=50)  
    produto_estoque = models.ForeignKey('cadastros.ProdutoBase',on_delete=models.SET_NULL,blank=True,null=True)


