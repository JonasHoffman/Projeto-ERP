from cadastros import views
from django.urls import path
from django.contrib.auth import views as auth_views

app_name = 'cadastros'
urlpatterns = [
    path("cadastrar_fornecedor/", views.cadastrar_fornecedor, name="cadastrar_fornecedor"),
    path("clientes/novo/", views.cadastrar_cliente, name="cadastrar_cliente"),
    path('regras_preco/novo/', views.cadastrar_regra_preco, name='cadastrar_regra_preco'),

    path('transportadoras/', views.transportadora_list, name='transportadora_list'),
    path('transportadoras/novo/', views.transportadora_create, name='transportadora_create'),
    path('transportadoras/<int:pk>/editar/', views.transportadora_update, name='transportadora_update'),

    path("produtos/", views.listar_produtos_base, name="listar_produtos_base"),
    path("produtos/novo/", views.cadastrar_produto_base, name="cadastrar_produto_base"),
    path("produtos/<int:pk>/editar/", views.editar_produto_base, name="editar_produto_base"),
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

    path('grupos/', views.grupo_produto_listar, name='grupo_produto_listar'),
    path('grupos/novo/', views.grupo_produto_criar, name='grupo_produto_criar'),
    path('grupos/<int:pk>/editar/', views.grupo_produto_editar, name='grupo_produto_editar'),

    # =========================
    # BANCOS
    # =========================
    path('bancos/', views.banco_list, name='banco_list'),
    path('bancos/novo/', views.banco_create, name='banco_create'),
    path('bancos/<int:pk>/editar/', views.banco_update, name='banco_update'),

    # =========================
    # CONTAS FINANCEIRAS
    # =========================
    path('contas-financeiras/', views.conta_list, name='conta_list'),
    path('contas-financeiras/novo/', views.conta_create, name='conta_create'),
    path('contas-financeiras/<int:pk>/editar/', views.conta_update, name='conta_update'),
]