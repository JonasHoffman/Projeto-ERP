from django.db import models
from cadastros.models import Cliente,Fornecedor,Banco,FormaPagamento
from vendas.models import Pedido,NFe
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.
class ContaReceber(models.Model):
    TIPO_CONTA_CHOICES = [
        ('Fatura', 'Fatura'),
        ('Boleto', 'Boleto'),
        ('Pix', 'Pix'),
    ]

    SITUACAO_CHOICES = [
        ('Aberta', 'Aberta'),
        ('Recebida', 'Recebida'),
        ('Atrasada', 'Atrasada'),
        ('Parcial', 'Parcial'),
    ]

    titulo = models.AutoField(primary_key=True)
    parcela = models.PositiveIntegerField(default=1)
    total_parcelas = models.PositiveIntegerField(default=1)
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True)
    nfe = models.ForeignKey(
        NFe, on_delete=models.SET_NULL, null=True, blank=True
    )
    pedido_numero = models.CharField(max_length=20, blank=True)
    tipo_conta = models.CharField(max_length=20, choices=TIPO_CONTA_CHOICES)
    situacao = models.CharField(max_length=20, choices=SITUACAO_CHOICES, default='Aberta')
    vencimento = models.DateField()
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)
    boleto_url = models.URLField(blank=True, null=True)
    criado_por = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
    charge_id = models.CharField(max_length=40, blank=True, null=True)
    
    def __str__(self):
        return f"Receber {self.titulo} - {self.cliente}"

    @property
    def total_recebido(self):
        return sum(r.valor_recebido for r in self.recebimentos.all())

    @property
    def saldo(self):
        return self.valor_total - self.total_recebido

    def atualizar_situacao(self):
        total_recebido = self.recebimentos.aggregate(total=models.Sum('valor_recebido'))['total'] or 0

        if total_recebido >= self.valor_total:
            self.situacao = 'Recebida'
        elif total_recebido > 0:
            self.situacao = 'Parcial'
        elif self.vencimento < timezone.now().date():
            self.situacao = 'Atrasada'
        else:
            self.situacao = 'Aberta'

        self.save(update_fields=['situacao'])


class Recebimento(models.Model):
    TIPO_LANCAMENTO = [
        ('NORMAL', 'Normal'),
        ('ESTORNO', 'Estorno'),
    ]

    conta = models.ForeignKey(ContaReceber, on_delete=models.CASCADE, related_name='recebimentos')
    data_recebimento = models.DateField(default=timezone.now)

    valor_recebido = models.DecimalField(max_digits=10, decimal_places=2)
    forma_recebimento = models.ForeignKey(
    FormaPagamento,
    on_delete=models.PROTECT
    )
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    tipo_lancamento = models.CharField(max_length=10, choices=TIPO_LANCAMENTO, default='NORMAL')
    observacao = models.TextField(blank=True, null=True)
    estorna_de = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='estornos'
    )

    def __str__(self):
        sinal = '-' if self.tipo_lancamento == 'ESTORNO' else ''
        return f"{sinal}R${self.valor_recebido} - {self.conta.titulo}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.conta.atualizar_situacao()

class ContasPagar(models.Model):
    TIPO_CONTA_CHOICES = [
        ('Fatura', 'Fatura'),
        ('Boleto', 'Boleto'),
        ('Pix', 'Pix'),
    ]

    SITUACAO_CHOICES = [
        ('Aberta', 'Aberta'),
        ('Paga', 'Paga'),
        ('Atrasada', 'Atrasada'),
        ('Parcial', 'Parcial'),
    ]

    titulo = models.AutoField(primary_key=True)
    cod_cliente = models.ForeignKey(Fornecedor, on_delete=models.SET_NULL, null=True)
    cod_banco = models.ForeignKey(Banco, on_delete=models.SET_NULL, null=True)
    forma_pagamento = models.ForeignKey(FormaPagamento, on_delete=models.SET_NULL, null=True)
    tipo_conta = models.CharField(max_length=20, choices=TIPO_CONTA_CHOICES)
    situacao = models.CharField(max_length=20, choices=SITUACAO_CHOICES, default='Aberta')
    dt_vencimento = models.DateField("Data de Vencimento",null=True)
    total_titulo = models.DecimalField("Valor total", max_digits=10, decimal_places=2)
    multa = models.DecimalField("Multa", max_digits=10, decimal_places=2, default=0)
    criado_por = models.ForeignKey(User, on_delete=models.CASCADE, editable=False,null=True,blank=True)

    def __str__(self):
        return f"Título {self.titulo} - {self.cod_cliente}"

    @property
    def total_pago(self):
        return sum(p.valor_pago for p in self.pagamentos.all())

    @property
    def saldo(self):
        return self.total_titulo - self.total_pago

    def atualizar_situacao(self):
        total_pago = self.pagamentos.aggregate(total=models.Sum('valor_pago'))['total'] or 0

        if total_pago >= self.total_titulo:
            self.situacao = 'Paga'
        elif total_pago > 0:
            self.situacao = 'Parcial'
        elif self.dt_vencimento < timezone.now().date():
            self.situacao = 'Atrasada'
        else:
            self.situacao = 'Aberta'

        self.save(update_fields=['situacao'])


class Pagamento(models.Model):
    TIPO_LANCAMENTO = [
        ('NORMAL', 'Normal'),
        ('ESTORNO', 'Estorno'),
    ]

    conta = models.ForeignKey(ContasPagar, on_delete=models.CASCADE, related_name='pagamentos')
    data_pagamento = models.DateField(auto_now_add=True)
    valor_pago = models.DecimalField(max_digits=10, decimal_places=2)
    forma_pagamento = models.ForeignKey(
    FormaPagamento,
    on_delete=models.PROTECT
    )
    pagamento_origem = models.OneToOneField(
        'self',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name='estorno'
    )
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    tipo_lancamento = models.CharField(max_length=10, choices=TIPO_LANCAMENTO, default='NORMAL')
    observacao = models.TextField(blank=True, null=True)

    def __str__(self):
        sinal = '-' if self.tipo_lancamento == 'ESTORNO' else ''
        return f"{sinal}R${self.valor_pago} - {self.conta.titulo}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.conta.atualizar_situacao()
