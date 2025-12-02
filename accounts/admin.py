from django.contrib import admin
from .models import SistemaModulo, SistemaView, PermissaoView


@admin.register(SistemaModulo)
class SistemaModuloAdmin(admin.ModelAdmin):
    list_display = ("id", "codigo", "nome")
    search_fields = ("codigo", "nome")


@admin.register(SistemaView)
class SistemaViewAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "rota", "modulo")
    list_filter = ("modulo",)
    search_fields = ("nome", "rota")


@admin.register(PermissaoView)
class PermissaoViewAdmin(admin.ModelAdmin):
    list_display = ("id", "view", "grupo", "usuario", "pode_acessar")
    list_filter = ("pode_acessar", "grupo", "usuario", "view")
    search_fields = ("view__nome",)