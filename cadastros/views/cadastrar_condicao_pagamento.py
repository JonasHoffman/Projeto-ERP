from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
from cadastros.models import TipoCliente, TabelaPreco, FormaPagamento, CondicaoPagamento

class CondicaoPagamentoListView(ListView):
    model = CondicaoPagamento
    template_name = "cadastro_condicao_pagamento.html"
    context_object_name = "condicoes_pagamento"

class CondicaoPagamentoCreateView(CreateView):
    model = CondicaoPagamento
    fields = ['codigo', 'nome', 'forma_pagamento', 'dias_vencimento', 'ativo']
    template_name = "cadastro_condicao_pagamento_form.html"
    success_url = reverse_lazy('cadastros:condicao_pagamento_list')

class CondicaoPagamentoUpdateView(UpdateView):
    model = CondicaoPagamento
    fields = ['codigo', 'nome', 'forma_pagamento', 'dias_vencimento', 'ativo']
    template_name = "cadastro_condicao_pagamento_form.html"
    success_url = reverse_lazy('cadastros:condicao_pagamento_list')
