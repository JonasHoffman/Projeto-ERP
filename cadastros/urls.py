from cadastros import views
from django.urls import path
from django.contrib.auth import views as auth_views

app_name = 'cadastros'
urlpatterns = [
    path("cadastrar_fornecedor/", views.cadastrar_fornecedor, name="cadastrar_forncedor"),
    path("clientes/novo/", views.cadastrar_cliente, name="cadastrar_cliente"),
    path('regras_preco/novo/', views.cadastrar_regra_preco, name='cadastrar_regra_preco'),
]