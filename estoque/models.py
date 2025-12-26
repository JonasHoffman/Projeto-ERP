from django.db import models
from django.contrib.auth.models import User
from django.apps import apps
from cadastros.models import ProdutoBase,Fornecedor,Deposito
from decimal import Decimal


# Create your models here.

class ProdutoEntrada(models.Model):
    produto = models.ForeignKey(ProdutoBase, on_delete=models.CASCADE)
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.SET_NULL, null=True, blank=True)
    fornecedor_nome = models.CharField(max_length=25)
    quantidade = models.DecimalField(max_digits=10, decimal_places=2)
    custo_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    custo_total = models.DecimalField(max_digits=10, decimal_places=2)
    lote = models.CharField(max_length=25, unique=False)
    deposito = models.ForeignKey(Deposito, on_delete=models.SET_NULL, null=True, blank=True)
    data_entrada = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.produto.codigo} - {self.lote}"
    
    def save(self,*args,**kwargs):
        if self.fornecedor:
            self.fornecedor_nome = self.fornecedor.nome_fantasia
        super().save(*args,**kwargs)
        
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
    fornecedor = models.ForeignKey(
    Fornecedor,
    on_delete=models.PROTECT
    )   
    produto_estoque = models.ForeignKey(ProdutoBase, on_delete=models.PROTECT)
    codigo_produto = models.CharField(max_length=50)

    class Meta:
        unique_together = ('fornecedor', 'codigo_produto')

    def __str__(self):
        return f"{self.fornecedor.nome_fantasia} - {self.codigo_produto}"


class NotaFiscalEntrada(models.Model):
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.PROTECT)
    numero = models.CharField(max_length=20)
    serie = models.CharField(max_length=10, blank=True, null=True)
    chave = models.CharField(max_length=60, unique=False)
    data_emissao = models.DateField(blank=True, null=True)

    valor_total = models.DecimalField(max_digits=12, decimal_places=2)
    valor_produtos = models.DecimalField(max_digits=12, decimal_places=2)

    xml = models.TextField()  # opcional
    pdf = models.FileField(upload_to="nfe_pdfs/", blank=True, null=True)

    criado_em = models.DateTimeField(auto_now_add=True)
    importado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"NF {self.numero} - {self.fornecedor.nome_fantasia}"
    
