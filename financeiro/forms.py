from django import forms
from financeiro.models import ContasPagar
from django import forms


class ContasPagarForm(forms.ModelForm):
    class Meta:
        model = ContasPagar
        fields = [
            'cod_cliente',
            'cod_banco',
            'forma_pagamento',
            'tipo_conta',
            'situacao',
            'dt_vencimento',
            'total_titulo',
            'multa',
        ]
        widgets = {
            'cod_cliente': forms.Select(attrs={'class': 'form-control'}),
            'cod_banco': forms.Select(attrs={'class': 'form-control'}),
            'forma_pagamento': forms.Select(attrs={'class': 'form-control'}),
            'tipo_conta': forms.Select(attrs={'class': 'form-control'}),
            'situacao': forms.Select(attrs={'class': 'form-control'}),
            'dt_vencimento': forms.DateInput(
                attrs={
                    'type': 'date',  # 🗓️ mostra o calendário pequeno
                    'class': 'form-control',
                    'style': 'width: 180px;'
                }
            ),
            'total_titulo': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'multa': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }
