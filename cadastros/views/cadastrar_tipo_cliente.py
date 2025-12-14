# cadastros/views.py
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
from cadastros.models import TipoCliente, TabelaPreco, FormaPagamento, CondicaoPagamento

# -----------------------------
# Tipo Cliente
# -----------------------------
class TipoClienteListView(ListView):
    model = TipoCliente
    template_name = "cadastro_tipo_cliente.html"
    context_object_name = "tipos_clientes"

class TipoClienteCreateView(CreateView):
    model = TipoCliente
    fields = ['codigo', 'descricao']
    template_name = "cadastro_tipo_cliente_form.html"
    success_url = reverse_lazy('tipo_cliente_list')

class TipoClienteUpdateView(UpdateView):
    model = TipoCliente
    fields = ['codigo', 'descricao']
    template_name = "cadastro_tipo_cliente_form.html"
    success_url = reverse_lazy('tipo_cliente_list')
