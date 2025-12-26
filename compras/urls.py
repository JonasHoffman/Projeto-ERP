from compras import views
from django.urls import path
from django.contrib.auth import views as auth_views

app_name = 'compras'
urlpatterns = [
    path('compras/', views.compras_em_aberto, name='compras_em_aberto'),
    path('compras/novo/', views.compras_criar_pedido, name='compras_criar_pedido'),
    path('compras/selecionar/', views.selecionar_compras_em_aberto, name='selecionar_compras_criar_pedido'),
    path('compras/<int:pedido_id>/', views.compras_detalhe_pedido, name='compras_detalhe_pedido'),
    path('compras/<int:pedido_id>/editar/', views.compras_editar_pedido, name='compras_editar_pedido'),
    path('compras/<int:pedido_id>/adicionar-item/', views.compras_adicionar_item, name='compras_adicionar_item'),
    path('compras/<int:pedido_id>/remover-item/<int:item_id>/', views.compras_remover_item, name='compras_remover_item'),
    path('pedido/<int:pedido_id>/adicionar_antecipacao/', views.compras_adicionar_antecipacao, name='compras_adicionar_antecipacao'),



    


]
