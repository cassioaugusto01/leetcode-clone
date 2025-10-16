from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Problem(models.Model):
    """Modelo para representar um desafio de programação"""
    DIFFICULTY_CHOICES = [
        ('easy', 'Fácil'),
        ('medium', 'Médio'),
        ('hard', 'Difícil'),
    ]
    
    title = models.CharField(max_length=200, verbose_name='Título')
    slug = models.SlugField(unique=True, verbose_name='Slug')
    description = models.TextField(verbose_name='Descrição')
    difficulty = models.CharField(
        max_length=10, 
        choices=DIFFICULTY_CHOICES, 
        default='medium',
        verbose_name='Dificuldade'
    )
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Data de Criação')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Data de Atualização')
    
    # Template inicial para o código
    starter_code = models.TextField(
        default='def solution():\n    # Escreva seu código aqui\n    pass',
        verbose_name='Código Inicial'
    )
    
    # Função que será chamada para testar
    function_name = models.CharField(
        max_length=100, 
        default='solution',
        verbose_name='Nome da Função'
    )
    
    class Meta:
        verbose_name = 'Desafio'
        verbose_name_plural = 'Desafios'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def get_solved_count(self):
        """Retorna o número de usuários que resolveram este desafio"""
        return Submission.objects.filter(
            problem=self, 
            status='accepted'
        ).values('user').distinct().count()


class TestCase(models.Model):
    """Modelo para representar casos de teste de um desafio"""
    problem = models.ForeignKey(
        Problem, 
        on_delete=models.CASCADE, 
        related_name='test_cases',
        verbose_name='Desafio'
    )
    input_data = models.TextField(verbose_name='Entrada (JSON)')
    expected_output = models.TextField(verbose_name='Saída Esperada (JSON)')
    is_sample = models.BooleanField(
        default=False, 
        verbose_name='Caso de Teste de Exemplo'
    )
    description = models.CharField(
        max_length=200, 
        blank=True,
        verbose_name='Descrição'
    )
    
    class Meta:
        verbose_name = 'Caso de Teste'
        verbose_name_plural = 'Casos de Teste'
        ordering = ['id']
    
    def __str__(self):
        return f"{self.problem.title} - Test {self.id}"


class Submission(models.Model):
    """Modelo para representar uma submissão de solução"""
    STATUS_CHOICES = [
        ('pending', 'Pendente'),
        ('running', 'Executando'),
        ('accepted', 'Aceito'),
        ('wrong_answer', 'Resposta Errada'),
        ('runtime_error', 'Erro de Execução'),
        ('time_limit', 'Tempo Limite Excedido'),
    ]
    
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        verbose_name='Usuário'
    )
    problem = models.ForeignKey(
        Problem, 
        on_delete=models.CASCADE,
        verbose_name='Desafio'
    )
    code = models.TextField(verbose_name='Código')
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending',
        verbose_name='Status'
    )
    result_message = models.TextField(
        blank=True,
        verbose_name='Mensagem de Resultado'
    )
    submitted_at = models.DateTimeField(
        default=timezone.now,
        verbose_name='Data de Submissão'
    )
    execution_time = models.FloatField(
        null=True, 
        blank=True,
        verbose_name='Tempo de Execução (segundos)'
    )
    
    class Meta:
        verbose_name = 'Submissão'
        verbose_name_plural = 'Submissões'
        ordering = ['-submitted_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.problem.title} - {self.status}"


class UserProfile(models.Model):
    """Modelo para estender as informações do usuário"""
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
        verbose_name='Usuário'
    )
    problems_solved = models.IntegerField(
        default=0,
        verbose_name='Desafios Resolvidos'
    )
    total_submissions = models.IntegerField(
        default=0,
        verbose_name='Total de Submissões'
    )
    
    class Meta:
        verbose_name = 'Perfil de Usuário'
        verbose_name_plural = 'Perfis de Usuário'
    
    def __str__(self):
        return f"Perfil de {self.user.username}"

