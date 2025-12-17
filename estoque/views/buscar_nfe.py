from django.shortcuts import render
from .services import sefaz_consultar_notas

def consultar_nfe_view(request):
    notas = None
    erro = None

    if request.method == "POST":
        cnpj = request.POST.get("cnpj")
        certificado = request.POST.get("certificado")  # pode deixar vazio por enquanto
        senha = request.POST.get("senha")  # idem

        if not cnpj:
            erro = "Informe um CNPJ para consultar."
        else:
            resposta = sefaz_consultar_notas(cnpj, certificado, senha)

            if resposta.get("ok"):
                notas = resposta.get("notas")
            else:
                erro = "Erro ao consultar notas na SEFAZ."

    return render(request, 'recebimento/buscar_nfe.html', {
        "notas": notas,
        "erro": erro,
    })
