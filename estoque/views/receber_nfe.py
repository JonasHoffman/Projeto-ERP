from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
import xmltodict
from decimal import Decimal
from estoque.models import ProdutoFornecedor, ProdutoBase, ProdutoEntradaTemp, Fornecedor, ProdutoEntrada
from estoque.forms import UploadNFeForm
from estoque.models import NotaFiscalEntrada

def receber_nfe(request):

    print("\n\n===================== IMPORTAR_NFE - INÍCIO =====================")
    print("Método:", request.method)
    print("POST keys:", list(request.POST.keys()))
    print("Tem xml_gerado?", "xml_gerado" in request.POST)

    # ----------------------------------------------------------
    # 0. XML vindo da consulta SEFAZ (xml_gerado)
    # ----------------------------------------------------------
    xml_gerado = request.POST.get("xml_gerado")
    if xml_gerado:
        print("xml_gerado RECEBIDO, tamanho:", len(xml_gerado))

        request.session["xml_temp"] = xml_gerado
        print("xml_temp salvo na sessão.")

        print("===================== IMPORTAR_NFE - FIM =====================\n\n")
        return redirect("estoque:receber_nfe")  # volta para GET

    # ----------------------------------------------------------
    # 1. Voltamos do redirect, XML está na sessão
    # ----------------------------------------------------------
    xml_temp = request.session.get('xml_temp')

    print("xml_temp existe na sessão?", xml_temp is not None)
    if xml_temp:
        print("Tamanho xml_temp:", len(xml_temp))
    print("===================== DEBUG INICIAL FIM =====================")

    if xml_temp:
        try:
            print("\n#### PARSING XML DA SESSÃO ####")
            xml_data = xmltodict.parse(xml_temp)

            print("Chaves do nível raiz:", list(xml_data.keys()))
            nfe = xml_data['nfeProc']['NFe']['infNFe']
            print("Chaves de infNFe:", list(nfe.keys()))

            emitente = nfe['emit']
            cnpj = emitente['CNPJ']
            numero_nf = nfe['ide']['nNF']

            print("Fornecedor CNPJ:", cnpj)
            print("Número NF:", numero_nf)

            # ----------------------------------------------------------
            # Verifica fornecedor
            # ----------------------------------------------------------
            fornecedor = Fornecedor.objects.filter(cnpj=cnpj).first()
            if not fornecedor:
                print("Fornecedor NÃO encontrado.")
                request.session['xml_temp'] = xml_temp
                messages.info(request, 'Fornecedor não cadastrado.')
                return redirect(f"{reverse('cadastros:cadastrar_fornecedor')}?next={request.path}")

            print("Fornecedor encontrado:", fornecedor.nome_fantasia)
            chave_acesso = nfe['@Id'].replace("NFe", "")  # vem como NFe3512... precisa remover prefixo
            valor_total_nf = Decimal(nfe['total']['ICMSTot']['vNF'])
            valor_produtos_nf = Decimal(nfe['total']['ICMSTot']['vProd'])
            data_emissao_nf = nfe['ide'].get('dEmi')

            
            print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',valor_total_nf)
            nf_registro, created = NotaFiscalEntrada.objects.get_or_create(
            chave=chave_acesso,   # chave é sempre única
            defaults={
                "fornecedor": fornecedor,
                "numero": numero_nf,
                "data_emissao": data_emissao_nf,
                "valor_total": valor_total_nf,
                "valor_produtos": valor_produtos_nf,
                "xml": xml_temp,
                "importado_por": request.user if request.user.is_authenticated else None
            }
            )

            if created:
                print("NF criada:", nf_registro.id)
            else:
                print("NF já existia, ID:", nf_registro.id)

            # ----------------------------------------------------------
            # Pegando produtos do XML
            # ----------------------------------------------------------
            produtos = nfe['det']

            print("\n#### DEBUG DET ####")
            print("Tipo de det:", type(produtos))
            print("Conteúdo bruto det:", produtos)

            if isinstance(produtos, dict):
                produtos = [produtos]

            print("Total de itens DET:", len(produtos))

            produtos_nao_relacionados = []

            for item in produtos:
                print("\n==== ITEM XML ====")
                print(item)

                prod = item["prod"]
                codigo_fornecedor = prod["cProd"]
                nome = prod["xProd"]

                print("Código fornecedor:", codigo_fornecedor)
                print("Nome produto:", nome)

                correspondencia = ProdutoFornecedor.objects.filter(
                    fornecedor=fornecedor,
                    codigo_produto__iexact=str(codigo_fornecedor).strip()
                ).first()

                if not correspondencia:
                    produtos_nao_relacionados.append({
                        "codigo": codigo_fornecedor,
                        "nome": nome
                    })

            print("\n#### RESULTADO BUSCA PRODUTOS ####")
            print("Produtos não relacionados:", produtos_nao_relacionados)

            if produtos_nao_relacionados:
                print("REDIRECIONANDO para tela de relacionar.")
                request.session['produtos_nao_encontrados'] = produtos_nao_relacionados
                request.session['fornecedor_cnpj'] = cnpj
                return redirect(f"{reverse('estoque:relacionar')}?next={request.path}")

            # ----------------------------------------------------------
            # Todos os produtos relacionados → criar registro temporário
            # ----------------------------------------------------------
            print("\n#### CRIANDO LANCAMENTOS TEMP ####")

            for item in produtos:
                prod = item['prod']

                codigo = prod['cProd']
                quantidade = Decimal(prod['qCom'])
                valor_unitario = Decimal(prod['vUnCom'])
                valor_total = Decimal(prod['vProd'])

                print(f"Salvando item: {codigo} | Qtd: {quantidade} | VlrUnit: {valor_unitario}")

                correspondencia = ProdutoFornecedor.objects.get(
                    fornecedor=fornecedor,
                    codigo_produto=codigo
                )
                produto_estoque = correspondencia.produto_estoque

                ProdutoEntradaTemp.objects.create(
                    produto=produto_estoque,
                    fornecedor=fornecedor,
                    quantidade=quantidade,
                    custo_unitario=valor_unitario,
                    custo_total=valor_total,
                    numero_nf=numero_nf,
                    finalizado=False,
                    recebido=request.user,
                )

            # ----------------------------------------------------------
            # Limpa sessão
            # ----------------------------------------------------------
            print("Limpando sessão...")
            request.session.pop('xml_temp', None)
            request.session.pop('produtos_nao_encontrados', None)
            request.session.pop('fornecedor_cnpj', None)

            print("Renderizando tela final...")

            return render(request, 'recebimento/formset_padrao_cadastro.html', {
                'numero_nf': numero_nf
            })

        except Exception as e:
            print("\n##### ERRO AO PROCESSAR XML #####")
            print(str(e))
            request.session.pop('xml_temp', None)
            return render(request, 'recebimento/formset_padrao_cadastro.html', {
                'erro': str(e)
            })

    # ----------------------------------------------------------
    # 2. Upload normal
    # ----------------------------------------------------------
    if request.method == 'POST':
        form = UploadNFeForm(request.POST, request.FILES)

        if form.is_valid():
            xml_file = form.cleaned_data['xml_file']
            xml_content = xml_file.read().decode('utf-8')

            print("\n### XML enviado via upload ###")
            print("Tamanho:", len(xml_content))

            request.session['xml_temp'] = xml_content
            return redirect("estoque:receber_nfe")

    else:
        form = UploadNFeForm()

    print("===================== IMPORTAR_NFE - FIM =====================\n\n")
    return render(request, 'recebimento/buscar_nfe.html', {'form': form})
