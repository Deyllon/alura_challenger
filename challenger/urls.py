from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("detalhes/<int:pk>", views.detalhes, name="detalhes"),
    path("transacoes_suspeitas/", views.transacoes_suspeitas, name="suspeitas")
]