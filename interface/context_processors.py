from interface.models import MenuItem, NavTop
from accounts.models import PermissaoView
from django.contrib.auth.models import Group

def menu_items(request):

    user = request.user
    menus = MenuItem.objects.prefetch_related('subitens').all()

    # Não filtra se o usuário não estiver logado (ex.: página de login)
    if not user.is_authenticated:
        for menu in menus:
            menu.subitens_permitidos = []
        return {'menus': menus}

    # Permissões por usuário
    permissoes_user = PermissaoView.objects.filter(
        usuario=user,
        permitido=True
    ).values_list("view_id", flat=True)

    # Permissões por grupo
    permissoes_grupos = PermissaoView.objects.filter(
        grupo__in=user.groups.all(),
        permitido=True
    ).values_list("view_id", flat=True)

    permissoes_ids = set(list(permissoes_user) + list(permissoes_grupos))

    # Adiciona a lista filtrada em cada menu
    for menu in menus:
        menu.subitens_permitidos = menu.subitens.filter(id__in=permissoes_ids)

    return {'menus': menus}


def nav_top(request):
    nav_ = NavTop.objects.all()
    return {'nav': nav_}
