from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, F
import json
from .forms import ProfessorRegistrationForm
from .models import Aluno, Notas
from django.contrib.auth import logout

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

# Página para adicionar notas
@login_required(login_url='login')
def adicionar_notas(request):
    try:
        if request.method == 'POST':
            # Criar novo aluno
            nome_aluno = request.POST.get('nome')
            if not nome_aluno:
                raise ValueError('O nome do aluno é obrigatório')
                
            aluno = Aluno.objects.create(nome=nome_aluno)
            
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
            
            return redirect('adicionar_notas')

        # Estatísticas básicas
        total_alunos = Aluno.objects.count()
        total_aprovados = (
            Notas.objects
            .annotate(media=(F('nota1') + F('nota2') + F('nota3')) / 3)
            .filter(media__gte=7)
            .values('aluno')
            .distinct()
            .count()
        )
        media_turma = (
            Notas.objects
            .annotate(media=(F('nota1') + F('nota2') + F('nota3')) / 3)
            .aggregate(media_geral=Avg('media'))['media_geral'] or 0
        )

        context = {
            'professor_nome': request.user.username,
            'total_alunos': total_alunos,
            'total_aprovados': total_aprovados,
            'total_reprovados': total_alunos - total_aprovados,
            'media_turma': round(media_turma, 2),
        }
        
        return render(request, 'notas/adicionar_notas.html', context)
    except Exception as e:
        print(f"Erro em adicionar_notas: {str(e)}")
        return render(request, 'notas/adicionar_notas.html', {
            'error': str(e),
            'professor_nome': request.user.username
        })

# Página para visualizar notas
@login_required
def visualizar_notas(request):
    try:
        alunos = Aluno.objects.all()
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
                'notas': notas_por_semestre,
                'media_final': round(media_final, 2),
            })

        return render(request, 'notas/visualizar_notas.html', {'alunos': data})
    except Exception as e:
        return render(request, 'notas/visualizar_notas.html', {'error': str(e)})
