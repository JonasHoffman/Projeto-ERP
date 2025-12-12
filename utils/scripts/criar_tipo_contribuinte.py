from cadastros.models import TipoCliente

dados = [
    ("DIS", "Distribuidor"),
    ("VAR", "Varejo"),
    ("ATA", "Atacado"),
    ("IND", "Indústria"),
    ("REV", "Revenda"),
    ("CON", "Consumidor Final"),
    ("SER", "Prestador de Serviços"),
    ("AGR", "Agronegócio"),
    ("GOV", "Governo"),
    ("ONG", "ONG / Instituições"),
]

for codigo, descricao in dados:
    TipoCliente.objects.create(codigo=codigo, descricao=descricao)