from cadastros.models import Banco

# Lista de 10 bancos de exemplo (código e nome)
bancos_exemplo = [
    ("001", "Banco do Brasil"),
    ("033", "Santander"),
    ("104", "Caixa Econômica Federal"),
    ("237", "Bradesco"),
    ("341", "Itaú Unibanco"),
    ("356", "Real"),
    ("399", "HSBC"),
    ("422", "Safra"),
    ("453", "Banco Rural"),
    ("633", "Banco Rendimento")
]

# Cria os bancos no banco de dados
for codigo, nome in bancos_exemplo:
    Banco.objects.get_or_create(codigo=codigo, defaults={"nome": nome})

print("10 bancos criados com sucesso!")
