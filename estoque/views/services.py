import random
from datetime import datetime, timedelta

def gerar_itens_fake():
    itens = []
    quantidade_itens = random.randint(1, 5)

    for i in range(1, quantidade_itens + 1):
        quantidade = round(random.uniform(1, 20), 2)
        valor_unit = round(random.uniform(5, 150), 2)
        total = round(quantidade * valor_unit, 2)

        itens.append({
            "nItem": i,
            "codigo": str(random.randint(1000, 9999)),
            "descricao": f"Produto Teste {random.randint(1, 99)}",
            "ncm": "84099930",
            "cfop": "5102",
            "unidade": "UN",
            "quantidade": quantidade,
            "valor_unitario": valor_unit,
            "valor_total": total,
        })

    return itens


def gerar_xml_fake(nota):
    """
    Gera um XML FAKE totalmente compatível com NF-e real.
    Compatível com sua view importar_nfe.
    """

    itens_xml = ""

    for item in nota["itens"]:
        itens_xml += f"""
        <det nItem="{item['nItem']}">
            <prod>
                <cProd>{item['codigo']}</cProd>
                <cEAN>SEM GTIN</cEAN>
                <xProd>{item['descricao']}</xProd>
                <NCM>{item['ncm']}</NCM>
                <CFOP>{item['cfop']}</CFOP>
                <uCom>{item['unidade']}</uCom>
                <qCom>{item['quantidade']}</qCom>
                <vUnCom>{item['valor_unitario']}</vUnCom>
                <vProd>{item['valor_total']}</vProd>
                <uTrib>{item['unidade']}</uTrib>
                <qTrib>{item['quantidade']}</qTrib>
                <vUnTrib>{item['valor_unitario']}</vUnTrib>
            </prod>
        </det>
        """

    xml = f"""
    <nfeProc xmlns="http://www.portalfiscal.inf.br/nfe" versao="4.00">
      <NFe>
        <infNFe Id="NFe{nota['chave']}" versao="4.00">
          <ide>
            <cUF>42</cUF>
            <cNF>1234</cNF>
            <natOp>VENDA</natOp>
            <mod>55</mod>
            <serie>{nota['serie']}</serie>
            <nNF>{nota['numero']}</nNF>
            <dhEmi>{nota['data_emissao'].strftime('%Y-%m-%dT%H:%M:%S-03:00')}</dhEmi>
            <tpNF>1</tpNF>
            <idDest>1</idDest>
            <tpImp>1</tpImp>
            <tpEmis>1</tpEmis>
            <tpAmb>2</tpAmb>
            <finNFe>1</finNFe>
            <indFinal>0</indFinal>
            <indPres>1</indPres>
          </ide>
          <emit>
            <CNPJ>123456780001</CNPJ>
            <xNome>{nota['emitente']}</xNome>
            <enderEmit>
              <xLgr>Rua Teste</xLgr>
              <nro>123</nro>
              <xBairro>Centro</xBairro>
              <cMun>4205407</cMun>
              <xMun>FakeCity</xMun>
              <UF>SC</UF>
              <CEP>89120000</CEP>
              <cPais>1058</cPais>
              <xPais>BRASIL</xPais>
              <fone>47999999999</fone>
            </enderEmit>
            <IE>123456789</IE>
            <CRT>3</CRT>
          </emit>
          <dest>
            <CNPJ>111111110001</CNPJ>
            <xNome>Cliente Exemplo LTDA</xNome>
            <enderDest>
              <xLgr>Av Central</xLgr>
              <nro>555</nro>
              <xBairro>Centro</xBairro>
              <cMun>4205407</cMun>
              <xMun>FakeCity</xMun>
              <UF>SC</UF>
              <CEP>89120000</CEP>
              <cPais>1058</cPais>
              <xPais>BRASIL</xPais>
              <fone>47988887777</fone>
            </enderDest>
            <indIEDest>1</indIEDest>
            <IE>999999999</IE>
          </dest>

          {itens_xml}

          <total>
            <ICMSTot>
              <vBC>0.00</vBC>
              <vICMS>0.00</vICMS>
              <vProd>{nota['valor_total']}</vProd>
              <vNF>{nota['valor_total']}</vNF>
            </ICMSTot>
          </total>
        </infNFe>
      </NFe>
    </nfeProc>
    """

    return xml.strip()


def gerar_nota_fake():
    itens = gerar_itens_fake()
    total = sum(i["valor_total"] for i in itens)

    chave = "".join([str(random.randint(0, 9)) for _ in range(44)])

    nota = {
        "chave": chave,
        "emitente": f"Fornecedor {random.choice(['ABC', 'XYZ', 'Comercial BR', 'GlobalTec'])} LTDA",
        "numero": str(random.randint(1000, 9999)),
        "serie": "1",
        "valor_total": round(total, 2),
        "data_emissao": datetime.now() - timedelta(days=random.randint(0, 10)),
        "status": "AUTORIZADA",
        "itens": itens,
    }

    nota["xml_fake"] = gerar_xml_fake(nota)
    return nota


def sefaz_consultar_notas(cnpj, certificado, senha):
    notas = [gerar_nota_fake() for _ in range(5)]
    return {"ok": True, "notas": notas}
