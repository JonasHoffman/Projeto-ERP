from django.shortcuts import render

def sem_permissao(request):
    return render(request, "permissoes/sem_permissao.html")