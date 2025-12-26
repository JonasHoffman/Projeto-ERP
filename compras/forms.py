from django import forms
from django.forms import inlineformset_factory
from compras.models import (
    PedidoCompra,
    PedidoCompraItem,
    PedidoCompraAntecipacao
)


class PedidoCompraForm(forms.ModelForm):
    class Meta:
        model = PedidoCompra
        fields = ['fornecedor']


class PedidoCompraItemForm(forms.ModelForm):
    codigo_produto = forms.CharField(
        label="Código do Produto",
        required=True,
        widget=forms.TextInput(attrs={
            "class": "codigo-produto",
            "autocomplete": "off",
            "placeholder": "Digite o código"
        })
    )

    class Meta:
        model = PedidoCompraItem
        fields = ['codigo_produto', 'produto', 'quantidade', 'valor_unitario']
        widgets = {
            'produto': forms.HiddenInput(),  # o produto real fica hidden
        }

    def clean(self):
        cleaned = super().clean()
        codigo = cleaned.get("codigo_produto")
        produto = cleaned.get("produto")

        if codigo and not produto:
            raise forms.ValidationError("Produto não encontrado")

        return cleaned


PedidoItemFormSet = inlineformset_factory(
    PedidoCompra,
    PedidoCompraItem,
    form=PedidoCompraItemForm,
    extra=1,
    can_delete=True
)


class PedidoCompraAntecipacaoForm(forms.ModelForm):
    class Meta:
        model = PedidoCompraAntecipacao
        fields = ['valor', 'observacao']
