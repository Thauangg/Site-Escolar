from django.urls import path
from .views import (
    home,
    adicionar_notas,
    visualizar_notas,
    register,
    login_view,
    logout_view,
    deletar_notas,
    adicionar_turma,
    visualizar_turmas,
)

urlpatterns = [
    # Página inicial
    path('', home, name='home'),

    # Rotas para notas
    path('adicionar_turma/', adicionar_turma, name='adicionar_turma'),
    path('visualizar_turmas/', visualizar_turmas, name='visualizar_turmas'),
    path('adicionar_notas/', adicionar_notas, name='adicionar_notas'),
    path('visualizar_notas/', visualizar_notas, name='visualizar_notas'),
    path('deletar_notas/<int:aluno_id>/', deletar_notas, name='deletar_notas'),

    # Rotas de autenticação
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]
