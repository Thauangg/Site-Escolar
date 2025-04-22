from django.urls import path
from .views import (
    home,
    adicionar_notas,
    visualizar_notas,
    register,
    login_view,
    logout_view,
)

urlpatterns = [
    # Página inicial
    path('', home, name='home'),

    # Rotas para notas
    path('adicionar_notas/', adicionar_notas, name='adicionar_notas'),
    path('visualizar_notas/', visualizar_notas, name='visualizar_notas'),

    # Rotas de autenticação
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]
