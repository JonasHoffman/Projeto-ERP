from django.db import models

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
            self.fornecedor_nome = self.fornecedor.nome
        super().save(*args,**kwargs)
# models.py
class ProdutoEntradaTemp(models.Model):
    produto = models.ForeignKey(ProdutoBase, on_delete=models.CASCADE)
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.CASCADE)
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

    produto = models.ForeignKey(ProdutoBase, on_delete=models.CASCADE)
    lote = models.CharField(max_length=25, null=True, blank=True)  # opcional
    deposito = models.ForeignKey(Deposito, on_delete=models.SET_NULL, null=True, blank=True)
    tipo = models.CharField(max_length=20, choices=TIPO)
    quantidade = models.DecimalField(max_digits=10, decimal_places=2)
    motivo = models.CharField(max_length=255, null=True, blank=True)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    data = models.DateTimeField(auto_now_add=True)

class ProdutoFornecedor(models.Model):
    cnpj_fornecedor = models.ForeignKey(Fornecedor,on_delete=models.SET_NULL,blank=True,null=True)
    nome_produto = models.CharField(max_length=50) 
    codigo_produto = models.CharField(max_length=50)  
    produto_estoque = models.ForeignKey(ProdutoBase,on_delete=models.SET_NULL,blank=True,null=True)


class Endereco(models.Model):
    logradouro = models.CharField(max_length=200)
    numero = models.CharField(max_length=20)
    complemento = models.CharField(max_length=100, blank=True, null=True)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)
    cep = models.CharField(max_length=15)

class Fornecedor(models.Model):

    SITUACAO_CHOICES = (
        ('ATIVO', 'Ativo'),
        ('INATIVO', 'Inativo'),
        ('BLOQUEADO', 'Bloqueado'),
    )

    nome_fantasia = models.CharField(max_length=100, default='Fornecedor Padrão')
    razao_social = models.CharField(max_length=100, default='Fornecedor Padrão')

    cnpj = models.CharField(max_length=18)
    inscricao_estadual = models.CharField(max_length=20, blank=True, null=True)
    inscricao_municipal = models.CharField(max_length=20, blank=True, null=True)

    email = models.EmailField(blank=True, null=True)

    # -----------------------------
    # Relacionamentos externos
    # -----------------------------
    endereco = models.ForeignKey(
        'cadastros.Endereco',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    banco_padrao = models.ForeignKey(
        'cadastros.Banco',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    transportadora = models.ForeignKey(
        'cadastros.Transportadora',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    contato = models.ForeignKey(
        'cadastros.Contato',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    situacao = models.CharField(
        max_length=10,
        choices=SITUACAO_CHOICES,
        default='ATIVO'
    )

    FRETE_CHOICES = (
        ('CIF', 'CIF - Remetente assume frete'),
        ('FOB', 'FOB - Destinatário assume frete'),
        ('OUTRO', 'Outro'),
    )

    # ... (restante dos campos)

    frete = models.CharField(
        max_length=10,
        choices=FRETE_CHOICES,
        default='CIF',
        blank=True,
        null=True
    )


    def __str__(self):
        return f"{self.nome_fantasia} ({self.cnpj})"