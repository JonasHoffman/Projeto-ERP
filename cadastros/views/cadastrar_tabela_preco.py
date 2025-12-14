# cadastros/views.py
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
from cadastros.models import TipoCliente, TabelaPreco, FormaPagamento, CondicaoPagamento

class TabelaPrecoListView(ListView):
    model = TabelaPreco
    template_name = "cadastro_tabela_preco.html"
    context_object_name = "tabelas_preco"

class TabelaPrecoCreateView(CreateView):
    model = TabelaPreco
    fields = ['nome']
    template_name = "cadastro_tabela_preco_form.html"
    success_url = reverse_lazy('cadastros:tabela_preco_list')

class TabelaPrecoUpdateView(UpdateView):
    model = TabelaPreco
    fields = ['nome']
    template_name = "cadastro_tabela_preco_form.html"
    success_url = reverse_lazy('cadastros:tabela_preco_list')