from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, F
import json
from .forms import ProfessorRegistrationForm
from .models import Aluno, Notas, Turma
from django.contrib.auth import logout
from django.contrib import messages

# Página inicial
def home(request):
    return render(request, 'notas/home.html')  # Mostra a página inicial

# Registro de usuários
def register(request):
    if request.method == 'POST':
        form = ProfessorRegistrationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)
                return redirect('adicionar_notas')
            except Exception as e:
                return render(request, 'notas/register.html', {
                    'form': form,
                    'error': f'Erro ao criar usuário: {str(e)}'
                })
        else:
            return render(request, 'notas/register.html', {
                'form': form,
                'error': 'Por favor, corrija os erros abaixo.'
            })
    else:
        form = ProfessorRegistrationForm()
    return render(request, 'notas/register.html', {'form': form})

# Login de usuários
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        next_url = request.POST.get('next', 'adicionar_notas')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(next_url)
        else:
            return render(request, 'notas/login.html', {
                'error': 'Credenciais inválidas',
                'next': next_url
            })
    
    next_url = request.GET.get('next', 'adicionar_notas')
    return render(request, 'notas/login.html', {'next': next_url})

# Logout de usuários
def logout_view(request):
    logout(request)  # Realiza o logout do usuário
    return redirect('login')  # Redireciona para a página de login

# Página para adicionar turmas
@login_required
def adicionar_turma(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        if nome:
            try:
                turma = Turma.objects.create(
                    nome=nome,
                    professor=request.user
                )
                messages.success(request, f'Turma "{nome}" criada com sucesso!')
                return redirect('adicionar_turma')
            except Exception as e:
                messages.error(request, f'Erro ao criar turma: {str(e)}')
        else:
            messages.error(request, 'O nome da turma é obrigatório')

    # Lista todas as turmas do professor
    turmas = Turma.objects.filter(professor=request.user).order_by('-data_criacao')
    return render(request, 'notas/adicionar_turma.html', {'turmas': turmas})

# Página para adicionar notas
@login_required
def adicionar_notas(request):
    try:
        if request.method == 'POST':
            # Verificar se existe uma turma selecionada
            turma_id = request.POST.get('turma')
            if not turma_id:
                raise ValueError('Selecione uma turma para adicionar o aluno')

            # Criar novo aluno
            nome_aluno = request.POST.get('nome')
            if not nome_aluno:
                raise ValueError('O nome do aluno é obrigatório')
            
            turma = Turma.objects.get(id=turma_id, professor=request.user)
            aluno = Aluno.objects.create(nome=nome_aluno, turma=turma)
            
            # Salvar notas para cada semestre
            for semestre in range(1, 4):
                nota1 = float(request.POST.get(f'sem{semestre}_nota1', 0))
                nota2 = float(request.POST.get(f'sem{semestre}_nota2', 0))
                nota3 = float(request.POST.get(f'sem{semestre}_nota3', 0))
                
                # Validar notas
                if not (0 <= nota1 <= 10 and 0 <= nota2 <= 10 and 0 <= nota3 <= 10):
                    raise ValueError(f'As notas do {semestre}º semestre devem estar entre 0 e 10')
                
                Notas.objects.create(
                    aluno=aluno,
                    professor=request.user,
                    semestre=semestre,
                    nota1=nota1,
                    nota2=nota2,
                    nota3=nota3
                )
            
            messages.success(request, f'Aluno {nome_aluno} adicionado com sucesso!')
            return redirect('visualizar_turmas')

        # Buscar todas as turmas do professor
        turmas = Turma.objects.filter(professor=request.user)
        
        # Verificar se veio da página de visualizar turmas
        turma_id = request.GET.get('turma')
        turma_selecionada = None
        if turma_id:
            try:
                turma_selecionada = Turma.objects.get(id=turma_id, professor=request.user)
            except Turma.DoesNotExist:
                pass

        context = {
            'professor_nome': request.user.username,
            'turmas': turmas,
            'turma_selecionada': turma_selecionada
        }
        
        return render(request, 'notas/adicionar_notas.html', context)
    except Exception as e:
        messages.error(request, str(e))
        return render(request, 'notas/adicionar_notas.html', {
            'professor_nome': request.user.username,
            'turmas': Turma.objects.filter(professor=request.user)
        })

# Página para visualizar notas
@login_required
def visualizar_notas(request):
    try:
        turma_id = request.GET.get('turma')
        if not turma_id:
            messages.error(request, 'Selecione uma turma para visualizar as notas')
            return redirect('visualizar_turmas')

        turma = Turma.objects.get(id=turma_id, professor=request.user)
        alunos = Aluno.objects.filter(turma=turma)
        data = []

        for aluno in alunos:
            notas = Notas.objects.filter(aluno=aluno).order_by('semestre')
            notas_por_semestre = {
                nota.semestre: {
                    'nota1': nota.nota1,
                    'nota2': nota.nota2,
                    'nota3': nota.nota3,
                    'media': round((nota.nota1 + nota.nota2 + nota.nota3) / 3, 2),
                }
                for nota in notas
            }
            media_final = (
                sum(nota['media'] for nota in notas_por_semestre.values()) / len(notas_por_semestre)
                if notas_por_semestre else 0
            )

            data.append({
                'nome': aluno.nome,
                'id': aluno.id,
                'notas': notas_por_semestre,
                'media_final': round(media_final, 2),
            })

        return render(request, 'notas/visualizar_notas.html', {
            'alunos': data,
            'turma': turma,
            'professor_nome': request.user.username
        })
    except Exception as e:
        messages.error(request, f'Erro ao carregar notas: {str(e)}')
        return redirect('visualizar_turmas')

@login_required
def deletar_notas(request, aluno_id):
    try:
        if request.method == 'POST':
            password = request.POST.get('password')
            # Verifica se a senha está correta
            if not request.user.check_password(password):
                messages.error(request, 'Senha incorreta. Por favor, tente novamente.')
                return redirect('visualizar_notas')

            aluno = Aluno.objects.get(id=aluno_id)
            # Primeiro deleta as notas
            Notas.objects.filter(aluno=aluno).delete()
            # Depois deleta o aluno
            aluno.delete()
            messages.success(request, 'Aluno e suas notas foram deletados com sucesso!')
            return redirect('visualizar_notas')
    except Exception as e:
        messages.error(request, f'Erro ao deletar aluno e notas: {str(e)}')
        return redirect('visualizar_notas')

@login_required
def visualizar_turmas(request):
    try:
        # Buscar todas as turmas do professor
        turmas = Turma.objects.filter(professor=request.user).order_by('-data_criacao')
        
        # Para cada turma, calcular as médias dos alunos
        for turma in turmas:
            for aluno in turma.alunos.all():
                notas = Notas.objects.filter(aluno=aluno).order_by('semestre')
                notas_por_semestre = {
                    nota.semestre: {
                        'nota1': nota.nota1,
                        'nota2': nota.nota2,
                        'nota3': nota.nota3,
                        'media': round((nota.nota1 + nota.nota2 + nota.nota3) / 3, 2),
                    }
                    for nota in notas
                }
                media_final = (
                    sum(nota['media'] for nota in notas_por_semestre.values()) / len(notas_por_semestre)
                    if notas_por_semestre else 0
                )
                aluno.media_final = round(media_final, 2)

        return render(request, 'notas/visualizar_turmas.html', {
            'turmas': turmas,
            'professor_nome': request.user.username
        })
    except Exception as e:
        messages.error(request, f'Erro ao carregar turmas: {str(e)}')
        return render(request, 'notas/visualizar_turmas.html', {
            'turmas': [],
            'professor_nome': request.user.username
        })
