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
        'cadastros.EnderecoFornecedor',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="fornecedor_principal"
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

class TipoCliente(models.Model):
    codigo = models.CharField(max_length=5, unique=True)
    descricao = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Tipo de Cliente"
        verbose_name_plural = "Tipos de Cliente"
        ordering = ["descricao"]

    def __str__(self):
        return self.descricao

class TabelaPreco(models.Model):
    nome = models.CharField(max_length=15) 

class FormaPagamento(models.Model):
    nome = models.CharField(max_length=15) 

class Vendedor(models.Model):
    nome = models.CharField(max_length=100)
    codigo = models.CharField(max_length=10, unique=True)
    cpf = models.CharField(max_length=14, unique=True, blank=True, null=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    comissao_percentual = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    ativo = models.BooleanField(default=True)
    data_cadastro = models.DateTimeField(auto_now_add=True,null=True)

class Deposito(models.Model):
    codigo = models.CharField(max_length=10, unique=True)
    nome = models.CharField(max_length=100)
    descricao = models.CharField(max_length=255, blank=True, null=True)
    endereco = models.CharField(max_length=255, blank=True, null=True)
    ativo = models.BooleanField(default=True)
    data_cadastro = models.DateTimeField(auto_now_add=True,null=True)

    class Meta:
        ordering = ["nome"]
        verbose_name = "Depósito"
        verbose_name_plural = "Depósitos"

    def __str__(self):
        return f"{self.codigo} - {self.nome}"

class EnderecoCliente(models.Model):
    cliente = models.ForeignKey(
        'Cliente',
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

class Cliente(models.Model):
    TIPO_PESSOA = (("F", "Pessoa Física"), ("J", "Pessoa Jurídica"))
    
    codigo = models.CharField(max_length=10, unique=True)
    tipo_pessoa = models.CharField(max_length=1, choices=TIPO_PESSOA, default="F")
    nome = models.CharField(max_length=150)
    razao_social = models.CharField(max_length=150,null=True)
    inscricao_estadual = models.CharField(max_length=20, blank=True, null=True)
    cpf_cnpj = models.CharField(max_length=18, unique=True)
    email = models.EmailField(blank=True, null=True)
    tipo_cliente = models.ForeignKey(
        TipoCliente,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="clientes"
    )
    telefone = models.CharField(max_length=20, blank=True, null=True)
    endereco = models.ForeignKey(
        EnderecoCliente,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="cliente_principal"
    )

    tabela_preco = models.ForeignKey(TabelaPreco, on_delete=models.SET_NULL, null=True, blank=True, related_name="clientes")
    forma_pagamento = models.ForeignKey(FormaPagamento, on_delete=models.SET_NULL, null=True, blank=True, related_name="clientes")
    vendedor = models.ForeignKey(Vendedor, on_delete=models.SET_NULL, null=True, blank=True, related_name="clientes")
    data_cadastro = models.DateTimeField(auto_now_add=True,null=True)
    ativo = models.BooleanField(default=True)

    class Meta:
        ordering = ["nome"]
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

    def __str__(self):
        return f"{self.codigo} - {self.nome}"
    
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
    


