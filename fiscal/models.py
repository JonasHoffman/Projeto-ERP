from django.db import models

# Create your models here.
class NaturezaOperacao(models.Model):
    TIPO_OPERACAO = [
        ('ENTRADA', 'Entrada'),
        ('SAIDA', 'Saída'),
        ('INTERNA', 'Interna'),
    ]

    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=TIPO_OPERACAO)
    cfop_padrao = models.CharField(max_length=10, blank=True, null=True)
    cst_icms = models.CharField(max_length=5, blank=True, null=True)
    cst_pis = models.CharField(max_length=5, blank=True, null=True)
    cst_cofins = models.CharField(max_length=5, blank=True, null=True)

    movimenta_estoque = models.BooleanField(default=True)
    movimenta_financeiro = models.BooleanField(default=True)
    gera_nfe = models.BooleanField(default=True)
    descricao_nfe = models.CharField(max_length=200, blank=True, null=True)

    # Campos do FECOEP
    gera_fecoep = models.BooleanField(default=False)

    def __str__(self):
        return self.nome

class FecoepEstado(models.Model):
    estado = models.CharField(max_length=2)  # Ex: 'SP', 'RJ'
    cfop = models.CharField(max_length=10)   # opcional, se variar por CFOP
    aliquota = models.DecimalField(max_digits=5, decimal_places=2)  # exemplo: 2.00%

    def __str__(self):
        return f"{self.estado} - {self.aliquota}% - CFOP {self.cfop}"