from cadastros import views
from django.urls import path
from django.contrib.auth import views as auth_views

app_name = 'cadastros'
urlpatterns = [
    path("cadastrar_fornecedor/", views.cadastrar_fornecedor, name="cadastrar_forncedor"),
    path("clientes/novo/", views.cadastrar_cliente, name="cadastrar_cliente"),
    path('regras_preco/novo/', views.cadastrar_regra_preco, name='cadastrar_regra_preco'),


    # Tipo Cliente
    path('tipo-cliente/', views.TipoClienteListView.as_view(), name='tipo_cliente_list'),
    path('tipo-cliente/novo/', views.TipoClienteCreateView.as_view(), name='tipo_cliente_create'),
    path('tipo-cliente/<int:pk>/editar/', views.TipoClienteUpdateView.as_view(), name='tipo_cliente_update'),

    # Tabela Preço
    path('tabela-preco/', views.TabelaPrecoListView.as_view(), name='tabela_preco_list'),
    path('tabela-preco/novo/', views.TabelaPrecoCreateView.as_view(), name='tabela_preco_create'),
    path('tabela-preco/<int:pk>/editar/', views.TabelaPrecoUpdateView.as_view(), name='tabela_preco_update'),

    # Forma Pagamento
    path('forma-pagamento/', views.FormaPagamentoListView.as_view(), name='forma_pagamento_list'),
    path('forma-pagamento/novo/', views.FormaPagamentoCreateView.as_view(), name='forma_pagamento_create'),
    path('forma-pagamento/<int:pk>/editar/', views.FormaPagamentoUpdateView.as_view(), name='forma_pagamento_update'),

    # Condição Pagamento
    path('condicao-pagamento/', views.CondicaoPagamentoListView.as_view(), name='condicao_pagamento_list'),
    path('condicao-pagamento/novo/', views.CondicaoPagamentoCreateView.as_view(), name='condicao_pagamento_create'),
    path('condicao-pagamento/<int:pk>/editar/', views.CondicaoPagamentoUpdateView.as_view(), name='condicao_pagamento_update'),
]