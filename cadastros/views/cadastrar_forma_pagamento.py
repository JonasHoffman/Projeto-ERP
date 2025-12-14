# cadastros/views.py
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
from cadastros.models import TipoCliente, TabelaPreco, FormaPagamento, CondicaoPagamento

class FormaPagamentoListView(ListView):
    model = FormaPagamento
    template_name = "cadastro_forma_pagamento.html"
    context_object_name = "formas_pagamento"

class FormaPagamentoCreateView(CreateView):
    model = FormaPagamento
    fields = ['codigo', 'nome', 'gera_boleto', 'ativo']
    template_name = "cadastro_forma_pagamento_form.html"
    success_url = reverse_lazy('cadastros:forma_pagamento_list')

class FormaPagamentoUpdateView(UpdateView):
    model = FormaPagamento
    fields = ['codigo', 'nome', 'gera_boleto', 'ativo']
    template_name = "cadastro_forma_pagamento_form.html"
    success_url = reverse_lazy('cadastros:forma_pagamento_list')
