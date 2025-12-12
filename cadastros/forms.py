from django import forms
from django.forms import modelformset_factory
from cadastros.models import Fornecedor, EnderecoFornecedor, ContatoFornecedor,Cliente,EnderecoCliente,Contato
from django.forms import inlineformset_factory

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
    Cliente,
    EnderecoCliente,
    form=EnderecoClienteForm,
    extra=1,
    can_delete=False,
    
)
ContatoFormSet = inlineformset_factory(
    Cliente,
    Contato,
    form=ContatoForm,
    extra=1,
    can_delete=False,
)
