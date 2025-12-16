from django.db import models
from cadastros.models import Cliente,FormaPagamento,Frete,TabelaPreco,Contato
from fiscal.models import NaturezaOperacao
from django.contrib.auth.models import User

# Create your models here.
class Oportunidade(models.Model):
    STATUS_CHOICES = [
        ('novo', 'Novo'),
        ('negociacao', 'Em negociação'),
        ('ganha', 'Ganha'),
        ('perdida', 'Perdida'),
    ]
    ORIGEM_CHOICES = [
        ('cliente', 'Cliente entrou em contato'),
        ('vendedor', 'Vendedor entrou em contato'),
        ('outro', 'Outra origem'),
    ]

    codigo = models.AutoField(primary_key=True)  # código único da oportunidade
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    contato = models.ForeignKey(
        Contato,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Pessoa de referência do cliente para esta oportunidade"
    )
    descricao = models.TextField(blank=True, null=True)  # observações ou informações iniciais
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='novo')
    responsavel = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # quem criou
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    origem = models.CharField(max_length=20, choices=ORIGEM_CHOICES, default='cliente',
                              help_text="Como essa oportunidade surgiu")


    def __str__(self):
        return f"Oportunidade #{self.codigo} - {self.cliente.nome}"

    class Meta:
        ordering = ['-data_criacao']
        verbose_name = "Oportunidade"
        verbose_name_plural = "Oportunidades"
class Pedido(models.Model):
    STATUS_CHOICES = [
        ('PENDENTE', 'Pendente'),
        ('APROVADO', 'Aprovado'),
        ('SEPARADO', 'Separado'),
        ('CANCELADO', 'Cancelado'),
        ('ENTREGUE', 'Entregue'),
    ]
    numero_pedido = models.PositiveIntegerField(unique=True, editable=False)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
  
    natureza_operacao = models.ForeignKey(NaturezaOperacao, on_delete=models.PROTECT,null=True)
    tabela_pedido = models.ForeignKey(TabelaPreco, on_delete=models.SET_NULL, null=True, blank=True)
    forma_pagamento_pedido = models.ForeignKey(FormaPagamento, on_delete=models.SET_NULL, null=True, blank=False)
    vendedor = models.ForeignKey(User,on_delete=models.SET_NULL,blank=True,null=True)
    frete_pedido = models.ForeignKey(Frete, on_delete=models.SET_NULL, null=True, blank=False)
    data_pedido = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDENTE')
    valor = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    oportunidade = models.ForeignKey('Oportunidade', on_delete=models.SET_NULL, null=True, blank=True)

    # Responsáveis por área
    responsavel_aprovacao = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="aprovador")
    responsavel_separacao = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="separador")
    responsavel_entrega = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="entregador")


class NFe(models.Model):
    numero = models.CharField(max_length=20)
    serie = models.CharField(max_length=5, default='1')
    chave = models.CharField(max_length=44, unique=True, blank=True, null=True)

    data_emissao = models.DateField()
    data_vencimento = models.DateField(blank=True, null=True)

    valor_total = models.DecimalField(max_digits=10, decimal_places=2)

    pedido = models.ForeignKey(
        Pedido,
        on_delete=models.SET_NULL,
        null=True, blank=True
    )

    STATUS = [
        ('AUTORIZADA', 'Autorizada'),
        ('CANCELADA', 'Cancelada'),
        ('DENEGADA', 'Denegada'),
        ('INUTILIZADA', 'Inutilizada'),
    ]
    status = models.CharField(max_length=20, choices=STATUS, default='AUTORIZADA')

    xml = models.TextField(blank=True, null=True)