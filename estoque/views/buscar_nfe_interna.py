from django.shortcuts import render
from estoque.models import ProdutoEntradaTemp

def buscar_nf_interna(request):
    nfs = []

    if request.method == 'POST':
        
        # Busca distintas NFs ainda não finalizadas
        nfs = ProdutoEntradaTemp.objects.filter(finalizado=False).values_list('numero_nf', flat=True).distinct()

    return render(request,'recebimento/buscar_nf_interna.html',{'nfs': nfs})