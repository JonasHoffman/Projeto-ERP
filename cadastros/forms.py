from django import forms
from django.forms import modelformset_factory
from cadastros.models import Fornecedor, EnderecoFornecedor, ContatoFornecedor,Cliente,EnderecoCliente,Contato,RegraPreco,ESTADOS_BRASIL,DescontoCliente,Transportadora
from cadastros.models import Banco, ContaFinanceira,ProdutoBase,GrupoProduto
from django.forms import inlineformset_factory


class ProdutoBaseForm(forms.ModelForm):
    class Meta:
        model = ProdutoBase
        fields = [
        "codigo",
        "nome",
        "descricao",
        "ncm",
        "unidade",
        "grupo",
        "preco_base",
        "ativo",
        ]


widgets = {
"descricao": forms.Textarea(attrs={"rows": 3}),
}
class FornecedorForm(forms.ModelForm):
    class Meta:
        model = Fornecedor
        fields = [
            "nome_fantasia", "razao_social", "cnpj",
            "inscricao_estadual", "inscricao_municipal",
            "email", 
        ]


class EnderecoForm(forms.ModelForm):
    class Meta:
        model = EnderecoFornecedor
        exclude = ("fornecedor",)


class ContatoForm(forms.ModelForm):
    class Meta:
        model = ContatoFornecedor
        exclude = ("fornecedor",)


EnderecoFormSet = modelformset_factory(
    EnderecoFornecedor,
    form=EnderecoForm,
    extra=1,
    can_delete=True
)

ContatoFormSet = modelformset_factory(
    ContatoFornecedor,
    form=ContatoForm,
    extra=1,
    can_delete=True
)


##cliente

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = [
            "tipo_pessoa",
            "nome",
            "razao_social",
            "inscricao_estadual",
            "cpf_cnpj",
            "email",
            "telefone",
            
        ]

        labels = {
            "tipo_pessoa": "Tipo de Pessoa",
            "nome": "Nome",
            "razao_social": "Razão Social",
            "inscricao_estadual": "Inscrição Estadual (IE)",
            "cpf_cnpj": "CPF ou CNPJ",
            "email": "E-mail",
            "telefone": "Telefone",
            
        }


class EnderecoClienteForm(forms.ModelForm):
    class Meta:
        model = EnderecoCliente
        fields = [
            "cep",
            "logradouro",
            "numero",
            "complemento",
            "bairro",
            "cidade",
            "estado",
        ]

class ContatoForm(forms.ModelForm):
    class Meta:
        model = Contato
        fields = [
            "nome",
            "telefone",
            "email",
            "cargo",
            "cpf",
        ]
EnderecoFormSet = inlineformset_factory(
    Fornecedor,
    EnderecoFornecedor,
    form=EnderecoForm,
    extra=1,
    can_delete=True
)

ContatoFormSet = inlineformset_factory(
    Fornecedor,
    ContatoFornecedor,
    form=ContatoForm,
    extra=1,
    can_delete=True
)

class RegraPrecoForm(forms.ModelForm):
    class Meta:
        model = RegraPreco
        fields = [
            "tabela_preco",
            "estado",
            "tipo_cliente",
            "percentual",
            "ativo",
        ]
        widgets = {
            'estado': forms.Select(choices=[('', 'Todos os Estados')] + list(ESTADOS_BRASIL)),
            "percentual": forms.NumberInput(attrs={
                "step": "0.01",
                "placeholder": "Ex: 10 ou -5"
            })
        }
class DescontoClienteForm(forms.ModelForm):
    class Meta:
        model = DescontoCliente
        fields = [
            "percentual",
            "valor_minimo",
            
            "data_inicio",
            "data_fim",
            "ativo",
        ]
        widgets = {
            "percentual": forms.NumberInput(attrs={
                "step": "0.01",
                "placeholder": "Ex: 5"
            }),
            "valor_minimo": forms.NumberInput(attrs={
                "step": "0.01",
                "placeholder": "Ex: 10000"
            }),
        }

DescontoClienteFormSet = inlineformset_factory(
    Cliente,
    DescontoCliente,
    form=DescontoClienteForm,
    extra=1,
    can_delete=False
)




class TransportadoraForm(forms.ModelForm):
    class Meta:
        model = Transportadora
        fields = ['nome', 'cnpj', 'ativo']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'cnpj': forms.TextInput(attrs={'class': 'form-control'}),
            'ativo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class BancoForm(forms.ModelForm):
    class Meta:
        model = Banco
        fields = ['codigo', 'nome', 'ativo']

        widgets = {
            'codigo': forms.TextInput(attrs={
                'placeholder': 'Ex: 001'
            }),
            'nome': forms.TextInput(attrs={
                'placeholder': 'Nome do banco'
            }),
        }

class ContaFinanceiraForm(forms.ModelForm):
    class Meta:
        model = ContaFinanceira
        fields = ['codigo', 'descricao', 'tipo', 'banco', 'ativa']

        widgets = {
            'codigo': forms.TextInput(attrs={
                'placeholder': 'Ex: CX001'
            }),
            'descricao': forms.TextInput(attrs={
                'placeholder': 'Descrição da conta'
            }),
            'tipo': forms.Select(),
            'banco': forms.Select(),
        }

class GrupoProdutoForm(forms.ModelForm):
    class Meta:
        model = GrupoProduto
        fields = ['codigo', 'nome', 'ativo']
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'ativo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }