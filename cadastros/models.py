from django.db import models

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
class TipoContribuiente(models.Model):
    nome = models.CharField(max_length=15) 

class TabelaPreco(models.Model):
    nome = models.CharField(max_length=15) 

class FormaPagamento(models.Model):
    nome = models.CharField(max_length=15) 


class Cliente(models.Model):
    nome = models.CharField(max_length=15,default='Cliente Padrão')  
    cpf_cnpj = models.CharField(max_length=18, unique=True)
    endereco = models.CharField(max_length=255, blank=True, null=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    codigo = models.CharField(max_length=9999)
    deposito = models.ForeignKey(TipoContribuiente, on_delete=models.SET_NULL, null=True, blank=False)
    tabela_preco = models.ForeignKey(TabelaPreco, on_delete=models.SET_NULL, null=True, blank=False)
    forma_pagamento = models.ForeignKey(FormaPagamento, on_delete=models.SET_NULL, null=True, blank=False)
    vendedor = models.CharField(max_length=20, blank=True, null=True)
    tabela_preco = models.ForeignKey(TabelaPreco, on_delete=models.SET_NULL, null=True)
    

    
    def __str__(self):
        return self.nome
    
    def save(self, *args, **kwargs):
        if not self.codigo:
            ultimo = Cliente.objects.all().order_by('id').last()
            if ultimo:
                ultimo_num = int(ultimo.codigo) + 1
                self.codigo = str(ultimo_num)  # Ex: 000001
            else:
                self.codigo = "1"
        super().save(*args, **kwargs)

class Contato(models.Model):
    # 🔹 O cliente ainda pode não existir no momento do cadastro
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name="contatos",
        blank=True,
        null=True
    )
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    cargo = models.CharField(max_length=50, blank=True, null=True)
    cpf = models.DecimalField(max_digits=13, decimal_places=1)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.cliente:
            return f"{self.nome} ({self.cliente.nome})"
        return f"{self.nome} (sem cliente)"

class ContatoFornecedor(models.Model):
    fornecedor = models.ForeignKey(
        'cadastros.Fornecedor',
        on_delete=models.CASCADE,
        related_name='contatos'
    )

    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    cargo = models.CharField(max_length=50, blank=True, null=True)
    cpf = models.CharField(max_length=14, blank=True, null=True)

    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['nome']
        verbose_name = "Contato do Fornecedor"
        verbose_name_plural = "Contatos do Fornecedor"

    def __str__(self):
        return f"{self.nome} - {self.fornecedor.nome_fantasia}"
    
class EnderecoFornecedor(models.Model):
    fornecedor = models.ForeignKey(
        Fornecedor,
        on_delete=models.CASCADE,
        related_name="enderecos"
    )
    cep = models.CharField(max_length=9)
    logradouro = models.CharField(max_length=200)
    numero = models.CharField(max_length=20, blank=True, null=True)
    complemento = models.CharField(max_length=100, blank=True, null=True)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)
    

    def __str__(self):
        return f"{self.logradouro}, {self.numero} - {self.cidade}/{self.estado}"
#Produtos

class Transportadora(models.Model):
    nome = models.CharField(max_length=100)
    cnpj = models.CharField(max_length=20, blank=True, null=True, unique=True)

    def __str__(self):
        return self.nome

class Deposito(models.Model):
    codigo = models.CharField(max_length=10, blank=False,unique=True)
    nome = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.nome
class Grupo(models.Model):
    codigo = models.CharField(max_length=10, blank=False,unique=True)
    nome = models.CharField(max_length=30, unique=True)

class ProdutoBase(models.Model):
    codigo = models.CharField(max_length=30, unique=True)
    nome = models.CharField(max_length=100)
    ncm = models.CharField(max_length=10, blank=True)
    unidade = models.CharField(max_length=10, blank=True)
    grupo = models.ForeignKey(Grupo, on_delete=models.SET_NULL, null=True, blank=True)
    descriçao = models.CharField(max_length=25) 
    preco_venda = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    def __str__(self):
        return self.codigo
    
class Banco(models.Model):
    codigo = models.CharField(max_length=10, unique=True)
    nome = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.codigo} - {self.nome}"
    
class Endereco(models.Model):
    logradouro = models.CharField(max_length=200)
    numero = models.CharField(max_length=20)
    complemento = models.CharField(max_length=100, blank=True, null=True)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)
    cep = models.CharField(max_length=15)

