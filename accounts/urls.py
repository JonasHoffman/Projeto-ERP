from accounts import views
from django.urls import path
from django.contrib.auth import views as auth_views

app_name = 'accounts'
urlpatterns = [
    path("gerenciar_permissoes/", views.gerenciar_permissoes, name="gerenciar_permissoes"),
    path("carregar_views/<int:modulo_id>/", views.carregar_views, name="carregar_views"),
    path("salvar_permissao/", views.salvar_permissao, name="salvar_permissao"),
]
