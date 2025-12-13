from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# utils/choices.py (ou no próprio models.py)

ESTADOS_BRASIL = (
    ('AC', 'Acre'),
    ('AL', 'Alagoas'),
    ('AP', 'Amapá'),
    ('AM', 'Amazonas'),
    ('BA', 'Bahia'),
    ('CE', 'Ceará'),
    ('DF', 'Distrito Federal'),
    ('ES', 'Espírito Santo'),
    ('GO', 'Goiás'),
    ('MA', 'Maranhão'),
    ('MT', 'Mato Grosso'),
    ('MS', 'Mato Grosso do Sul'),
    ('MG', 'Minas Gerais'),
    ('PA', 'Pará'),
    ('PB', 'Paraíba'),
    ('PR', 'Paraná'),
    ('PE', 'Pernambuco'),
    ('PI', 'Piauí'),
    ('RJ', 'Rio de Janeiro'),
    ('RN', 'Rio Grande do Norte'),
    ('RS', 'Rio Grande do Sul'),
    ('RO', 'Rondônia'),
    ('RR', 'Roraima'),
    ('SC', 'Santa Catarina'),
    ('SP', 'São Paulo'),
    ('SE', 'Sergipe'),
    ('TO', 'Tocantins'),
)

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

    def __str__(self):
        return f"{self.nome}"

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
    estado = models.CharField(
        max_length=2,
        choices=ESTADOS_BRASIL,
        blank=False,
        null=False,
        help_text="Vazio = todos os estados"
    )

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
    percentual_ajuste = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ],
        help_text="Percentual de ajuste futuro (0 a 100)"
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

class DescontoCliente(models.Model):
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name="descontos"
    )

    percentual = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Ex: 5 = 5%"
    )

    valor_minimo = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        help_text="Valor mínimo do pedido para ativar o desconto"
    )

    ativo = models.BooleanField(default=True)

    data_inicio = models.DateField(blank=True, null=True)
    data_fim = models.DateField(blank=True, null=True)

    class Meta:
        verbose_name = "Desconto por Cliente"
        verbose_name_plural = "Descontos por Cliente"

    def __str__(self):
        return f"{self.percentual}% acima de {self.valor_minimo}"
    
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
    estado = models.CharField(
        max_length=2,
        choices=ESTADOS_BRASIL,
        blank=False,
        null=False,
        help_text="Vazio = todos os estados"
    )
    

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
    preco_base = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    def __str__(self):
        return self.codigo
    
class Banco(models.Model):
    codigo = models.CharField(max_length=10, unique=True)
    nome = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.codigo} - {self.nome}"
    
class RegraPreco(models.Model):
    tabela_preco = models.ForeignKey(
        TabelaPreco,
        on_delete=models.CASCADE,
        related_name="regras"
    )

    estado = models.CharField(
        max_length=2,
        blank=True,
        null=True,
        help_text="Ex: SP, RJ. Vazio = todos"
    )

    tipo_cliente = models.ForeignKey(
        TipoCliente,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        help_text="Ex: Atacado, Varejo. Vazio = todos"
    )

    percentual = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        help_text="Ex: 10 = +10%, -5 = -5%"
    )

    ativo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Regra de Preço"
        verbose_name_plural = "Regras de Preço"

    def nivel_especificidade(self):
        """
        Quanto mais campos preenchidos, mais específica
        """
        pontos = 0
        if self.estado:
            pontos += 1
        if self.tipo_cliente:
            pontos += 1
        return pontos

class ItemVenda(models.Model):
    # venda = models.ForeignKey('Venda', on_delete=models.CASCADE)
    produto = models.ForeignKey(ProdutoBase, on_delete=models.PROTECT)
    quantidade = models.DecimalField(max_digits=10, decimal_places=2)
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)
