from django.urls import path
from buscas import views

app_name = "busca"

urlpatterns = [
    path("clientes/", views.buscar_clientes, name="busca_clientes"),
    path("fornecedores/", views.buscar_fornecedores, name="busca_fornecedores"),
    path("transportadoras/", views.buscar_transportadoras, name="busca_transportadoras"),
    path("bancos/", views.buscar_bancos, name="busca_bancos"),
]