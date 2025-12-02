from django.shortcuts import redirect
from django.urls import resolve
from accounts.models import SistemaView, PermissaoView

class ViewPermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith("/accounts/gerenciar_permissoes/"):
            return self.get_response(request)

        if request.path.startswith("/accounts/carregar_views/"):
            return self.get_response(request)

        if request.path.startswith("/accounts/salvar_permissao/"):
            return self.get_response(request)
                # Ignorar static
        if request.path.startswith("/static/"):
            return self.get_response(request)

        # Ignorar rotas públicas
        PUBLIC_URLS = [
            "/accounts/login/",
            "/accounts/logout/",
            "/accounts/sem-permissao/",
        ]

        if request.path in PUBLIC_URLS:
            return self.get_response(request)

        # Ignorar rotas do painel de permissões
        if request.path.startswith("/accounts/carregar_views/"):
            return self.get_response(request)

        if request.path.startswith("/accounts/gerenciar_permissoes/"):
            return self.get_response(request)

        if request.path.startswith("/accounts/salvar_permissao/"):
            return self.get_response(request)

        # Se não estiver logado, libera (deixa o Django redirecionar)
        if not request.user.is_authenticated:
            return self.get_response(request)

        resolver = resolve(request.path_info)
        view_name = resolver.view_name

        # View não registrada → acesso liberado
        try:
            view_obj = SistemaView.objects.get(nome=view_name)
        except SistemaView.DoesNotExist:
            return self.get_response(request)

        grupos = request.user.groups.all()

        if PermissaoView.objects.filter(view=view_obj, grupo__in=grupos, pode_acessar=True).exists():
            return self.get_response(request)

        if PermissaoView.objects.filter(view=view_obj, usuario=request.user, pode_acessar=True).exists():
            return self.get_response(request)

        return redirect("sem_permissao")
