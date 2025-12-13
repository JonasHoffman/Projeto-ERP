# views.py
from django.shortcuts import render, redirect
from cadastros.models import RegraPreco
from cadastros.forms import RegraPrecoForm

def cadastrar_regra_preco(request):
    if request.method == "POST":
        form = RegraPrecoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("lista_regras_preco")
    else:
        form = RegraPrecoForm()

    return render(request, "cadastro_regra_preco.html", {
        "form": form
    })
