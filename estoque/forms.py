from django import forms
from django.forms import inlineformset_factory
from cadastros.models import ProdutoBase



class UploadNFeForm(forms.Form):
    xml_file = forms.FileField(label='Envie o arquivo XML')

class Relacionar_produto_FornecedorForm(forms.Form):
    codigo = forms.CharField(
        label='Código do fornecedor',
        required=False,
        widget=forms.TextInput(attrs={
            'readonly': 'readonly',
            'class': 'form-control'
        })
    )

    nome = forms.CharField(
        label='Nome do produto',
        required=False,
        widget=forms.TextInput(attrs={
            'readonly': 'readonly',
            'class': 'form-control'
        })
    )

    produto_estoque = forms.ModelChoiceField(
        queryset=ProdutoBase.objects.all(),
        label='Produto do sistema'
    )

class recebimento_em_estoqueForm(forms.Form):
    lote = forms.CharField(max_length=50)
    nr_embalagem = forms.CharField(max_length=50)
    quantidade_por_caixa = forms.CharField(max_length=50)