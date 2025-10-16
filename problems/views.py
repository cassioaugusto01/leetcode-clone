from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Count, Q
import json

from .models import Problem, TestCase, Submission, UserProfile
from .forms import UserRegistrationForm, CodeSubmissionForm
from .code_executor import execute_code


def home(request):
    """Página inicial"""
    problems_count = Problem.objects.count()
    users_count = UserProfile.objects.count()
    submissions_count = Submission.objects.count()
    
    recent_problems = Problem.objects.all()[:6]
    
    context = {
        'problems_count': problems_count,
        'users_count': users_count,
        'submissions_count': submissions_count,
        'recent_problems': recent_problems,
    }
    return render(request, 'problems/home.html', context)


def register(request):
    """Página de registro de usuário"""
    if request.user.is_authenticated:
        return redirect('problem_list')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Conta criada com sucesso para {username}!')
            login(request, user)
            return redirect('problem_list')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'problems/register.html', {'form': form})


def user_login(request):
    """Página de login"""
    if request.user.is_authenticated:
        return redirect('problem_list')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', 'problem_list')
            return redirect(next_url)
        else:
            messages.error(request, 'Usuário ou senha inválidos')
    
    return render(request, 'problems/login.html')


def user_logout(request):
    """Logout do usuário"""
    logout(request)
    messages.info(request, 'Você saiu da sua conta')
    return redirect('home')


def problem_list(request):
    """Lista todos os desafios"""
    problems = Problem.objects.all()
    
    # Filtro por dificuldade
    difficulty = request.GET.get('difficulty')
    if difficulty:
        problems = problems.filter(difficulty=difficulty)
    
    # Busca por título
    search = request.GET.get('search')
    if search:
        problems = problems.filter(
            Q(title__icontains=search) | Q(description__icontains=search)
        )
    
    # Adicionar informação se o usuário já resolveu
    if request.user.is_authenticated:
        solved_problems = Submission.objects.filter(
            user=request.user,
            status='accepted'
        ).values_list('problem_id', flat=True)
    else:
        solved_problems = []
    
    context = {
        'problems': problems,
        'solved_problems': solved_problems,
        'current_difficulty': difficulty,
        'search_query': search,
    }
    return render(request, 'problems/problem_list.html', context)


def problem_detail(request, slug):
    """Detalhe de um desafio específico"""
    problem = get_object_or_404(Problem, slug=slug)
    
    # Pegar apenas casos de teste de exemplo
    sample_test_cases = problem.test_cases.filter(is_sample=True)
    
    # Verificar se o usuário já resolveu
    user_solved = False
    user_submissions = []
    if request.user.is_authenticated:
        user_submissions = Submission.objects.filter(
            user=request.user,
            problem=problem
        ).order_by('-submitted_at')[:5]
        
        # Verificar se já resolveu (query separada, antes do slice)
        user_solved = Submission.objects.filter(
            user=request.user,
            problem=problem,
            status='accepted'
        ).exists()
    
    form = CodeSubmissionForm(initial={'code': problem.starter_code})
    
    context = {
        'problem': problem,
        'sample_test_cases': sample_test_cases,
        'form': form,
        'user_solved': user_solved,
        'user_submissions': user_submissions,
    }
    return render(request, 'problems/problem_detail.html', context)


@login_required
@require_POST
def run_code(request, slug):
    """Executa o código do usuário com casos de teste de exemplo"""
    problem = get_object_or_404(Problem, slug=slug)
    
    try:
        data = json.loads(request.body)
        code = data.get('code', '')
        
        if not code:
            return JsonResponse({'error': 'Código vazio'}, status=400)
        
        # Pegar apenas casos de teste de exemplo
        test_cases = problem.test_cases.filter(is_sample=True)
        
        if not test_cases.exists():
            return JsonResponse({'error': 'Nenhum caso de teste disponível'}, status=400)
        
        # Preparar casos de teste
        test_cases_data = [
            {
                'input_data': tc.input_data,
                'expected_output': tc.expected_output
            }
            for tc in test_cases
        ]
        
        # Executar código
        result = execute_code(code, test_cases_data, problem.function_name)
        
        return JsonResponse(result)
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
@require_POST
def submit_code(request, slug):
    """Submete o código do usuário para avaliação completa"""
    problem = get_object_or_404(Problem, slug=slug)
    
    try:
        data = json.loads(request.body)
        code = data.get('code', '')
        
        if not code:
            return JsonResponse({'error': 'Código vazio'}, status=400)
        
        # Criar submissão
        submission = Submission.objects.create(
            user=request.user,
            problem=problem,
            code=code,
            status='running'
        )
        
        # Pegar todos os casos de teste
        test_cases = problem.test_cases.all()
        
        if not test_cases.exists():
            submission.status = 'runtime_error'
            submission.result_message = 'Nenhum caso de teste disponível'
            submission.save()
            return JsonResponse({'error': 'Nenhum caso de teste disponível'}, status=400)
        
        # Preparar casos de teste
        test_cases_data = [
            {
                'input_data': tc.input_data,
                'expected_output': tc.expected_output
            }
            for tc in test_cases
        ]
        
        # Executar código
        result = execute_code(code, test_cases_data, problem.function_name)
        
        # Atualizar submissão
        submission.status = result['status']
        submission.result_message = result['message']
        submission.execution_time = result['execution_time']
        submission.save()
        
        # Atualizar perfil do usuário
        profile = request.user.userprofile
        profile.total_submissions += 1
        
        # Se foi aceito e é a primeira vez que resolve este desafio
        if result['status'] == 'accepted':
            previous_accepted = Submission.objects.filter(
                user=request.user,
                problem=problem,
                status='accepted'
            ).exclude(id=submission.id).exists()
            
            if not previous_accepted:
                profile.problems_solved += 1
        
        profile.save()
        
        return JsonResponse({
            'submission_id': submission.id,
            'status': submission.status,
            'message': submission.result_message,
            'execution_time': submission.execution_time,
            'test_results': result.get('test_results', [])
        })
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def user_profile(request):
    """Página de perfil do usuário"""
    profile = request.user.userprofile
    
    # Submissões recentes
    recent_submissions = Submission.objects.filter(
        user=request.user
    ).select_related('problem').order_by('-submitted_at')[:10]
    
    # Desafios resolvidos
    solved_problems = Submission.objects.filter(
        user=request.user,
        status='accepted'
    ).values('problem').distinct()
    
    solved_problem_ids = [sp['problem'] for sp in solved_problems]
    solved_problem_list = Problem.objects.filter(id__in=solved_problem_ids)
    
    context = {
        'profile': profile,
        'recent_submissions': recent_submissions,
        'solved_problems': solved_problem_list,
    }
    return render(request, 'problems/profile.html', context)


@login_required
def submission_detail(request, submission_id):
    """Detalhe de uma submissão"""
    submission = get_object_or_404(
        Submission, 
        id=submission_id,
        user=request.user
    )
    
    context = {
        'submission': submission,
    }
    return render(request, 'problems/submission_detail.html', context)

