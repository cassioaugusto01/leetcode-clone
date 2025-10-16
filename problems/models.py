from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Challenge(models.Model):
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
        db_table = 'problems_problem'  # Manter tabela existente
    
    def __str__(self):
        return self.title
    
    def get_solved_count(self):
        """Retorna o número de usuários que resolveram este desafio"""
        return Submission.objects.filter(
            challenge=self, 
            status='accepted'
        ).values('user').distinct().count()


# Manter alias Problem para compatibilidade
Problem = Challenge


class TestCase(models.Model):
    """Modelo para representar casos de teste de um desafio"""
    challenge = models.ForeignKey(
        Challenge, 
        on_delete=models.CASCADE, 
        related_name='test_cases',
        verbose_name='Desafio',
        db_column='problem_id'  # Manter coluna existente
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
        db_table = 'problems_testcase'  # Manter tabela existente
    
    def __str__(self):
        return f"{self.challenge.title} - Test {self.id}"
    
    # Propriedade para compatibilidade
    @property
    def problem(self):
        return self.challenge


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
    challenge = models.ForeignKey(
        Challenge, 
        on_delete=models.CASCADE,
        verbose_name='Desafio',
        db_column='problem_id'  # Manter coluna existente
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
        db_table = 'problems_submission'  # Manter tabela existente
    
    def __str__(self):
        return f"{self.user.username} - {self.challenge.title} - {self.status}"
    
    # Propriedade para compatibilidade
    @property
    def problem(self):
        return self.challenge


class UserProfile(models.Model):
    """Modelo para estender as informações do usuário"""
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
        verbose_name='Usuário'
    )
    challenges_solved = models.IntegerField(
        default=0,
        verbose_name='Desafios Resolvidos',
        db_column='problems_solved'  # Manter coluna existente
    )
    total_submissions = models.IntegerField(
        default=0,
        verbose_name='Total de Submissões'
    )
    
    class Meta:
        verbose_name = 'Perfil de Usuário'
        verbose_name_plural = 'Perfis de Usuário'
        db_table = 'problems_userprofile'  # Manter tabela existente
    
    def __str__(self):
        return f"Perfil de {self.user.username}"
    
    # Propriedade para compatibilidade
    @property
    def problems_solved(self):
        return self.challenges_solved
    
    @problems_solved.setter
    def problems_solved(self, value):
        self.challenges_solved = value

