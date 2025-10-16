from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from problems.models import Problem, TestCase as ProblemTestCase, Submission
import json


class HomeViewTest(TestCase):
    """Testes para a view home"""
    
    def setUp(self):
        self.client = Client()
    
    def test_home_view_status_code(self):
        """Testa se a página inicial carrega"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
    
    def test_home_view_template(self):
        """Testa se usa o template correto"""
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'problems/home.html')
    
    def test_home_view_context(self):
        """Testa se o contexto contém as variáveis corretas"""
        response = self.client.get(reverse('home'))
        self.assertIn('problems_count', response.context)
        self.assertIn('users_count', response.context)
        self.assertIn('submissions_count', response.context)


class RegisterViewTest(TestCase):
    """Testes para a view de registro"""
    
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')
    
    def test_register_view_get(self):
        """Testa acesso à página de registro"""
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'problems/register.html')
    
    def test_register_view_post_valid(self):
        """Testa registro com dados válidos"""
        data = {
            'username': 'newuser',
            'email': 'newuser@test.com',
            'password1': 'complexpass123',
            'password2': 'complexpass123'
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, 302)  # Redirect após sucesso
        self.assertTrue(User.objects.filter(username='newuser').exists())
    
    def test_register_creates_userprofile(self):
        """Testa se o perfil é criado automaticamente"""
        data = {
            'username': 'testuser',
            'email': 'test@test.com',
            'password1': 'complexpass123',
            'password2': 'complexpass123'
        }
        self.client.post(self.register_url, data)
        user = User.objects.get(username='testuser')
        self.assertTrue(hasattr(user, 'userprofile'))


class LoginViewTest(TestCase):
    """Testes para a view de login"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.login_url = reverse('login')
    
    def test_login_view_get(self):
        """Testa acesso à página de login"""
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'problems/login.html')
    
    def test_login_view_post_valid(self):
        """Testa login com credenciais válidas"""
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': '12345'
        })
        self.assertEqual(response.status_code, 302)  # Redirect após sucesso
    
    def test_login_view_post_invalid(self):
        """Testa login com credenciais inválidas"""
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'wrongpass'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Usuário ou senha inválidos')


class ProblemListViewTest(TestCase):
    """Testes para a view de lista de problemas"""
    
    def setUp(self):
        self.client = Client()
        Problem.objects.create(
            title='Problema 1',
            slug='problema-1',
            description='Descrição 1',
            difficulty='easy'
        )
        Problem.objects.create(
            title='Problema 2',
            slug='problema-2',
            description='Descrição 2',
            difficulty='hard'
        )
    
    def test_problem_list_view(self):
        """Testa listagem de problemas"""
        response = self.client.get(reverse('problem_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'problems/problem_list.html')
        self.assertEqual(len(response.context['problems']), 2)
    
    def test_problem_list_filter_difficulty(self):
        """Testa filtro por dificuldade"""
        response = self.client.get(reverse('problem_list') + '?difficulty=easy')
        self.assertEqual(len(response.context['problems']), 1)
        self.assertEqual(response.context['problems'][0].difficulty, 'easy')
    
    def test_problem_list_search(self):
        """Testa busca por título"""
        response = self.client.get(reverse('problem_list') + '?search=Problema 1')
        self.assertEqual(len(response.context['problems']), 1)


class ProblemDetailViewTest(TestCase):
    """Testes para a view de detalhe do problema"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.problem = Problem.objects.create(
            title='Teste',
            slug='teste',
            description='Descrição do teste',
            difficulty='easy',
            starter_code='def solution():\n    pass'
        )
        ProblemTestCase.objects.create(
            problem=self.problem,
            input_data='[1, 2]',
            expected_output='3',
            is_sample=True
        )
    
    def test_problem_detail_view(self):
        """Testa visualização de problema"""
        response = self.client.get(reverse('problem_detail', args=['teste']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'problems/problem_detail.html')
        self.assertEqual(response.context['problem'], self.problem)
    
    def test_problem_detail_with_authenticated_user(self):
        """Testa com usuário autenticado"""
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('problem_detail', args=['teste']))
        self.assertIn('user_submissions', response.context)
        self.assertIn('user_solved', response.context)


class RunCodeViewTest(TestCase):
    """Testes para a view de executar código"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.problem = Problem.objects.create(
            title='Soma',
            slug='soma',
            description='Somar',
            difficulty='easy',
            function_name='solution'
        )
        ProblemTestCase.objects.create(
            problem=self.problem,
            input_data='[2, 3]',
            expected_output='5',
            is_sample=True
        )
    
    def test_run_code_requires_login(self):
        """Testa se requer autenticação"""
        response = self.client.post(reverse('run_code', args=['soma']))
        self.assertEqual(response.status_code, 302)  # Redirect para login
    
    def test_run_code_with_valid_code(self):
        """Testa execução com código válido"""
        self.client.login(username='testuser', password='12345')
        data = {
            'code': 'def solution(a, b):\n    return a + b'
        }
        response = self.client.post(
            reverse('run_code', args=['soma']),
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertIn('status', result)
        self.assertIn('test_results', result)
    
    def test_run_code_with_empty_code(self):
        """Testa com código vazio"""
        self.client.login(username='testuser', password='12345')
        response = self.client.post(
            reverse('run_code', args=['soma']),
            data=json.dumps({'code': ''}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)


class SubmitCodeViewTest(TestCase):
    """Testes para a view de submeter código"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.problem = Problem.objects.create(
            title='Soma',
            slug='soma',
            description='Somar',
            difficulty='easy',
            function_name='solution'
        )
        ProblemTestCase.objects.create(
            problem=self.problem,
            input_data='[2, 3]',
            expected_output='5',
            is_sample=False
        )
    
    def test_submit_code_requires_login(self):
        """Testa se requer autenticação"""
        response = self.client.post(reverse('submit_code', args=['soma']))
        self.assertEqual(response.status_code, 302)
    
    def test_submit_code_creates_submission(self):
        """Testa se cria submissão"""
        self.client.login(username='testuser', password='12345')
        data = {
            'code': 'def solution(a, b):\n    return a + b'
        }
        response = self.client.post(
            reverse('submit_code', args=['soma']),
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Submission.objects.filter(user=self.user, problem=self.problem).exists())
    
    def test_submit_code_updates_profile(self):
        """Testa se atualiza perfil do usuário"""
        self.client.login(username='testuser', password='12345')
        profile = self.user.userprofile
        initial_submissions = profile.total_submissions
        
        data = {
            'code': 'def solution(a, b):\n    return a + b'
        }
        self.client.post(
            reverse('submit_code', args=['soma']),
            data=json.dumps(data),
            content_type='application/json'
        )
        
        profile.refresh_from_db()
        self.assertEqual(profile.total_submissions, initial_submissions + 1)


class UserProfileViewTest(TestCase):
    """Testes para a view de perfil do usuário"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
    
    def test_profile_requires_login(self):
        """Testa se requer autenticação"""
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 302)
    
    def test_profile_view(self):
        """Testa visualização do perfil"""
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'problems/profile.html')
        self.assertIn('profile', response.context)
        self.assertIn('recent_submissions', response.context)
        self.assertIn('solved_problems', response.context)

