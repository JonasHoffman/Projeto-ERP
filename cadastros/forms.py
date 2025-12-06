from django import forms
from django.forms import modelformset_factory
from cadastros.models import Fornecedor, EnderecoFornecedor, ContatoFornecedor

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