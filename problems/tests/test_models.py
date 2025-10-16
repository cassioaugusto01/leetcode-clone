from django.test import TestCase
from django.contrib.auth.models import User
from problems.models import Problem, TestCase as ProblemTestCase, Submission, UserProfile
import json


class ProblemModelTest(TestCase):
    """Testes para o modelo Problem"""
    
    def setUp(self):
        """Configuração inicial para os testes"""
        self.problem = Problem.objects.create(
            title='Teste Soma',
            slug='teste-soma',
            description='Somar dois números',
            difficulty='easy',
            starter_code='def solution(a, b):\n    pass',
            function_name='solution'
        )
    
    def test_problem_creation(self):
        """Testa criação de um problema"""
        self.assertEqual(self.problem.title, 'Teste Soma')
        self.assertEqual(self.problem.slug, 'teste-soma')
        self.assertEqual(self.problem.difficulty, 'easy')
        self.assertEqual(self.problem.function_name, 'solution')
    
    def test_problem_str(self):
        """Testa representação string do problema"""
        self.assertEqual(str(self.problem), 'Teste Soma')
    
    def test_problem_verbose_names(self):
        """Testa verbose names do problema"""
        self.assertEqual(Problem._meta.verbose_name, 'Desafio')
        self.assertEqual(Problem._meta.verbose_name_plural, 'Desafios')
    
    def test_get_solved_count(self):
        """Testa contagem de problemas resolvidos"""
        user = User.objects.create_user(username='testuser', password='12345')
        Submission.objects.create(
            user=user,
            problem=self.problem,
            code='def solution(a, b): return a + b',
            status='accepted'
        )
        self.assertEqual(self.problem.get_solved_count(), 1)
    
    def test_difficulty_choices(self):
        """Testa opções de dificuldade"""
        choices = dict(Problem.DIFFICULTY_CHOICES)
        self.assertIn('easy', choices)
        self.assertIn('medium', choices)
        self.assertIn('hard', choices)


class TestCaseModelTest(TestCase):
    """Testes para o modelo TestCase"""
    
    def setUp(self):
        """Configuração inicial"""
        self.problem = Problem.objects.create(
            title='Teste',
            slug='teste',
            description='Descrição',
            difficulty='easy'
        )
        self.test_case = ProblemTestCase.objects.create(
            problem=self.problem,
            input_data=json.dumps([2, 3]),
            expected_output=json.dumps(5),
            is_sample=True,
            description='Teste 2 + 3'
        )
    
    def test_testcase_creation(self):
        """Testa criação de caso de teste"""
        self.assertEqual(self.test_case.problem, self.problem)
        self.assertEqual(self.test_case.input_data, '[2, 3]')
        self.assertEqual(self.test_case.expected_output, '5')
        self.assertTrue(self.test_case.is_sample)
    
    def test_testcase_str(self):
        """Testa representação string do caso de teste"""
        expected = f"{self.problem.title} - Test {self.test_case.id}"
        self.assertEqual(str(self.test_case), expected)
    
    def test_testcase_verbose_names(self):
        """Testa verbose names"""
        self.assertEqual(ProblemTestCase._meta.verbose_name, 'Caso de Teste')
        self.assertEqual(ProblemTestCase._meta.verbose_name_plural, 'Casos de Teste')


class SubmissionModelTest(TestCase):
    """Testes para o modelo Submission"""
    
    def setUp(self):
        """Configuração inicial"""
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.problem = Problem.objects.create(
            title='Teste',
            slug='teste',
            description='Descrição',
            difficulty='easy'
        )
        self.submission = Submission.objects.create(
            user=self.user,
            problem=self.problem,
            code='def solution(a, b): return a + b',
            status='accepted',
            execution_time=0.05
        )
    
    def test_submission_creation(self):
        """Testa criação de submissão"""
        self.assertEqual(self.submission.user, self.user)
        self.assertEqual(self.submission.problem, self.problem)
        self.assertEqual(self.submission.status, 'accepted')
        self.assertEqual(self.submission.execution_time, 0.05)
    
    def test_submission_str(self):
        """Testa representação string"""
        expected = f"{self.user.username} - {self.problem.title} - accepted"
        self.assertEqual(str(self.submission), expected)
    
    def test_submission_status_choices(self):
        """Testa opções de status"""
        choices = dict(Submission.STATUS_CHOICES)
        self.assertIn('pending', choices)
        self.assertIn('running', choices)
        self.assertIn('accepted', choices)
        self.assertIn('wrong_answer', choices)
        self.assertIn('runtime_error', choices)
        self.assertIn('time_limit', choices)


class UserProfileModelTest(TestCase):
    """Testes para o modelo UserProfile"""
    
    def setUp(self):
        """Configuração inicial"""
        self.user = User.objects.create_user(username='testuser', password='12345')
    
    def test_userprofile_creation(self):
        """Testa criação automática de perfil via signal"""
        self.assertTrue(hasattr(self.user, 'userprofile'))
        self.assertEqual(self.user.userprofile.problems_solved, 0)
        self.assertEqual(self.user.userprofile.total_submissions, 0)
    
    def test_userprofile_str(self):
        """Testa representação string"""
        expected = f"Perfil de {self.user.username}"
        self.assertEqual(str(self.user.userprofile), expected)
    
    def test_userprofile_update(self):
        """Testa atualização de estatísticas"""
        profile = self.user.userprofile
        profile.problems_solved = 5
        profile.total_submissions = 10
        profile.save()
        
        profile.refresh_from_db()
        self.assertEqual(profile.problems_solved, 5)
        self.assertEqual(profile.total_submissions, 10)

