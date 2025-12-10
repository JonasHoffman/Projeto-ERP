from cadastros.models import Transportadora
import random

nomes = [
    "TransLog Express",
    "RotaSul Transportes",
    "ViaCargo Brasil",
    "Rapidão Entregas",
    "Brasil Norte Log",
    "CargaMax Transporte",
    "Expresso Horizonte",
    "LogServ Distribuição",
    "Rodoviário Santo André",
    "TransVale Solutions",
]

for nome in nomes:
    cnpj = f"{random.randint(10,99)}.{random.randint(100,999)}.{random.randint(100,999)}/0001-{random.randint(10,99)}"
    Transportadora.objects.create(nome=nome, cnpj=cnpj)

print("10 transportadoras criadas!")