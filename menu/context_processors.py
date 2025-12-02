from estoque.models import MenuItem,NavTop

def menu_items(request):
    menus = MenuItem.objects.prefetch_related('subitens').all()
    return {'menus': menus}

def nav_top(request):
    nav_ = NavTop.objects.all()
    return {'nav':nav_}