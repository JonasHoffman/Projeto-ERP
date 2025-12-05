from django.db import models

# Create your models here.
class Fornecedor(models.Model):
    nome = models.CharField(max_length=15,default='Fornecedor Padrão')  
    cnpj = models.CharField(max_length=200)

    def __str__(self):
        return self.nome
    
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