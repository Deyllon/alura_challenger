from django.urls import path
from . import views


urlpatterns = [
    path("cadastro/", views.cadastro, name="cadastro"),
    path("visualizar_usuarios", views.usuarios_cadastrados, name="usuarios_cadastrados"),
    path("editar_usuario/<int:pk>", views.editar_usuario, name="editar_usuarios"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("deletar/<str:email>", views.deletar, name="deletar")
]
