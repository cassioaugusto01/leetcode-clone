from django.test import TestCase
from django.contrib.auth.models import User
from problems.models import Challenge, TestCase as ChallengeTestCase, Submission, UserProfile
import json


class ChallengeModelTest(TestCase):
    """Testes para o modelo Challenge"""
    
    def setUp(self):
        """Configuração inicial para os testes"""
        self.challenge = Challenge.objects.create(
            title='Teste Soma',
            slug='teste-soma',
            description='Somar dois números',
            difficulty='easy',
            starter_code='def solution(a, b):\n    pass',
            function_name='solution'
        )
    
    def test_challenge_creation(self):
        """Testa criação de um desafio"""
        self.assertEqual(self.challenge.title, 'Teste Soma')
        self.assertEqual(self.challenge.slug, 'teste-soma')
        self.assertEqual(self.challenge.difficulty, 'easy')
        self.assertEqual(self.challenge.function_name, 'solution')
    
    def test_challenge_str(self):
        """Testa representação string do desafio"""
        self.assertEqual(str(self.challenge), 'Teste Soma')
    
    def test_challenge_verbose_names(self):
        """Testa verbose names do desafio"""
        self.assertEqual(Challenge._meta.verbose_name, 'Desafio')
        self.assertEqual(Challenge._meta.verbose_name_plural, 'Desafios')
    
    def test_get_solved_count(self):
        """Testa contagem de desafios resolvidos"""
        user = User.objects.create_user(username='testuser', password='12345')
        Submission.objects.create(
            user=user,
            challenge=self.challenge,
            code='def solution(a, b): return a + b',
            status='accepted'
        )
        self.assertEqual(self.challenge.get_solved_count(), 1)
    
    def test_difficulty_choices(self):
        """Testa opções de dificuldade"""
        choices = dict(Challenge.DIFFICULTY_CHOICES)
        self.assertIn('easy', choices)
        self.assertIn('medium', choices)
        self.assertIn('hard', choices)


class TestCaseModelTest(TestCase):
    """Testes para o modelo TestCase"""
    
    def setUp(self):
        """Configuração inicial"""
        self.challenge = Challenge.objects.create(
            title='Teste',
            slug='teste',
            description='Descrição',
            difficulty='easy'
        )
        self.test_case = ChallengeTestCase.objects.create(
            challenge=self.challenge,
            input_data=json.dumps([2, 3]),
            expected_output=json.dumps(5),
            is_sample=True,
            description='Teste 2 + 3'
        )
    
    def test_testcase_creation(self):
        """Testa criação de caso de teste"""
        self.assertEqual(self.test_case.challenge, self.challenge)
        self.assertEqual(self.test_case.input_data, '[2, 3]')
        self.assertEqual(self.test_case.expected_output, '5')
        self.assertTrue(self.test_case.is_sample)
    
    def test_testcase_str(self):
        """Testa representação string do caso de teste"""
        expected = f"{self.challenge.title} - Test {self.test_case.id}"
        self.assertEqual(str(self.test_case), expected)
    
    def test_testcase_verbose_names(self):
        """Testa verbose names"""
        self.assertEqual(ChallengeTestCase._meta.verbose_name, 'Caso de Teste')
        self.assertEqual(ChallengeTestCase._meta.verbose_name_plural, 'Casos de Teste')


class SubmissionModelTest(TestCase):
    """Testes para o modelo Submission"""
    
    def setUp(self):
        """Configuração inicial"""
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.challenge = Challenge.objects.create(
            title='Teste',
            slug='teste',
            description='Descrição',
            difficulty='easy'
        )
        self.submission = Submission.objects.create(
            user=self.user,
            challenge=self.challenge,
            code='def solution(a, b): return a + b',
            status='accepted',
            execution_time=0.05
        )
    
    def test_submission_creation(self):
        """Testa criação de submissão"""
        self.assertEqual(self.submission.user, self.user)
        self.assertEqual(self.submission.challenge, self.challenge)
        self.assertEqual(self.submission.status, 'accepted')
        self.assertEqual(self.submission.execution_time, 0.05)
    
    def test_submission_str(self):
        """Testa representação string"""
        expected = f"{self.user.username} - {self.challenge.title} - accepted"
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
        self.assertEqual(self.user.userprofile.challenges_solved, 0)
        self.assertEqual(self.user.userprofile.total_submissions, 0)
    
    def test_userprofile_str(self):
        """Testa representação string"""
        expected = f"Perfil de {self.user.username}"
        self.assertEqual(str(self.user.userprofile), expected)
    
    def test_userprofile_update(self):
        """Testa atualização de estatísticas"""
        profile = self.user.userprofile
        profile.challenges_solved = 5
        profile.total_submissions = 10
        profile.save()
        
        profile.refresh_from_db()
        self.assertEqual(profile.challenges_solved, 5)
        self.assertEqual(profile.total_submissions, 10)

