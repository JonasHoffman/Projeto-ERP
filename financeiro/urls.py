from django.urls import path
from . import views

urlpatterns = [
    path("gerar_boleto/<int:pedido_id>/", views.gerar_boleto, name="gerar_boleto"),
    path("contas_receber/", views.contas_receber, name="contas_receber"),
    path('contas_pagar/novo/', views.criar_conta_pagar, name='criar_conta_pagar'),
    path('conta/pagamento/', views.registrar_pagamentos, name='registrar_pagamentos'),
    path('pagamento/<int:pagamento_id>/estornar/', views.estornar_pagamento, name='estornar_pagamento'),
    path('contas/receber/', views.registrar_recebimentos, name='registrar_recebimentos'),
    path("estornar/<int:recebimento_id>/", views.estornar_recebimento, name="estornar_recebimento"),
    path('fluxo-caixa/', views.fluxo_caixa, name='fluxo_caixa'),
    path("gerar-boleto/<int:pedido_id>/", views.gerar_boleto, name="gerar_boleto"),
    path("gerar-boleto-teste/", views.gerar_boleto_teste, name="gerar_boleto_teste"),
    path("webhook/efi/", views.webhook_efi, name="webhook_efi"),
    # estoque/urls.py
    

    

]
