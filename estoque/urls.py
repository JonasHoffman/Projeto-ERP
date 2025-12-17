from estoque import views
from django.urls import path
from django.contrib.auth import views as auth_views

app_name = 'estoque'
urlpatterns = [
    path("buscar_nfe/", views.consultar_nfe_view, name="consultar_nfe"),
    path("receber_nfe/", views.receber_nfe, name="receber_nfe"),


    
]
