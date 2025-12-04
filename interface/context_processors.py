from interface.models import MenuItem, NavTop
from accounts.models import PermissaoView

def menu_items(request):

    user = request.user
    menus = MenuItem.objects.prefetch_related('subitens__view').all()

    # Usuário não logado → não mostra nada
    if not user.is_authenticated:
        for menu in menus:
            menu.subitens_permitidos = []
        return {'menus': menus}

    # Permissões por usuário
    permissoes_user = PermissaoView.objects.filter(
        usuario=user,
        pode_acessar=True
    ).values_list("view_id", flat=True)

    # Permissões pelos grupos do usuário
    permissoes_grupos = PermissaoView.objects.filter(
        grupo__in=user.groups.all(),
        pode_acessar=True
    ).values_list("view_id", flat=True)

    # Junta todos os IDs de view permitidos
    permissoes_ids = set(permissoes_user) | set(permissoes_grupos)

    # Filtra submenus
    for menu in menus:
        sub_permitidos = []
        for sub in menu.subitens.all():

            # Se o subitem não tem view associada → mostrar sempre
            if sub.view_id is None:
                sub_permitidos.append(sub)
                continue

            # Filtra submenus usando a view vinculada
            if sub.view_id in permissoes_ids:
                sub_permitidos.append(sub)

        menu.subitens_permitidos = sub_permitidos

    return {'menus': menus}


def nav_top(request):
    nav_ = NavTop.objects.all()
    return {'nav': nav_}
