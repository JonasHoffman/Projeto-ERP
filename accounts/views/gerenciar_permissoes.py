from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth.models import Group, User
from accounts.models import SistemaModulo, SistemaView, PermissaoView
from django.views.decorators.csrf import csrf_exempt


@login_required
def gerenciar_permissoes(request):

    grupos = Group.objects.all().order_by("name")
    usuarios = User.objects.filter(is_active=True).order_by("username")
    modulos = SistemaModulo.objects.all().order_by("nome")

    return render(request, "accounts/gerenciar_permissoes.html", {
        "grupos": grupos,
        "usuarios": usuarios,
        "modulos": modulos,
    })


def carregar_views(request, modulo_id):
    tipo = request.GET.get("tipo")       # "grupo" ou "usuario"
    alvo_id = request.GET.get("id")      # id do grupo ou do usuário

    modulo = get_object_or_404(SistemaModulo, id=modulo_id)
    views = SistemaView.objects.filter(modulo=modulo)

    resposta = []

    for v in views:
        pode = False

        if tipo == "grupo" and alvo_id:
            # busca permissão do grupo para esta view
            pode = PermissaoView.objects.filter(view=v, grupo_id=alvo_id, pode_acessar=True).exists()
        elif tipo == "usuario" and alvo_id:
            # busca permissão do usuário para esta view
            pode = PermissaoView.objects.filter(view=v, usuario_id=alvo_id, pode_acessar=True).exists()

        resposta.append({
            "id": v.id,
            "nome": v.nome,
            "rota": v.rota,
            "pode": pode   # ✅ true se o grupo/usuário tem acesso
        })

    return JsonResponse({"views": resposta})


@csrf_exempt
def salvar_permissao(request):
    if request.method == "POST":
        data = request.POST
        view_id = data.get("view_id")
        tipo = data.get("tipo")
        alvo_id = data.get("id")
        pode = data.get("pode") == "true"  # converte para boolean

        view = SistemaView.objects.get(id=view_id)

        if tipo == "grupo":
            grupo = Group.objects.get(id=alvo_id)
            permissao, created = PermissaoView.objects.get_or_create(
                view=view,
                grupo=grupo,
                usuario=None,
                defaults={"pode_acessar": pode}
            )
        elif tipo == "usuario":
            usuario = User.objects.get(id=alvo_id)
            permissao, created = PermissaoView.objects.get_or_create(
                view=view,
                usuario=usuario,
                grupo=None,
                defaults={"pode_acessar": pode}
            )
        # Se o registro já existia, atualiza o valor
        if not created:
            permissao.pode_acessar = pode
            permissao.save()

        return JsonResponse({"status": "ok"})