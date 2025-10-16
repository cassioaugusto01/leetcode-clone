# Generated migration file for problema -> desafio changes

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Título')),
                ('slug', models.SlugField(unique=True, verbose_name='Slug')),
                ('description', models.TextField(verbose_name='Descrição')),
                ('difficulty', models.CharField(choices=[('easy', 'Fácil'), ('medium', 'Médio'), ('hard', 'Difícil')], default='medium', max_length=10, verbose_name='Dificuldade')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Data de Criação')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Data de Atualização')),
                ('starter_code', models.TextField(default='def solution():\n    # Escreva seu código aqui\n    pass', verbose_name='Código Inicial')),
                ('function_name', models.CharField(default='solution', max_length=100, verbose_name='Nome da Função')),
            ],
            options={
                'verbose_name': 'Desafio',
                'verbose_name_plural': 'Desafios',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('problems_solved', models.IntegerField(default=0, verbose_name='Desafios Resolvidos')),
                ('total_submissions', models.IntegerField(default=0, verbose_name='Total de Submissões')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuário')),
            ],
            options={
                'verbose_name': 'Perfil de Usuário',
                'verbose_name_plural': 'Perfis de Usuário',
            },
        ),
        migrations.CreateModel(
            name='TestCase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('input_data', models.TextField(verbose_name='Entrada (JSON)')),
                ('expected_output', models.TextField(verbose_name='Saída Esperada (JSON)')),
                ('is_sample', models.BooleanField(default=False, verbose_name='Caso de Teste de Exemplo')),
                ('description', models.CharField(blank=True, max_length=200, verbose_name='Descrição')),
                ('problem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='test_cases', to='problems.problem', verbose_name='Desafio')),
            ],
            options={
                'verbose_name': 'Caso de Teste',
                'verbose_name_plural': 'Casos de Teste',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.TextField(verbose_name='Código')),
                ('status', models.CharField(choices=[('pending', 'Pendente'), ('running', 'Executando'), ('accepted', 'Aceito'), ('wrong_answer', 'Resposta Errada'), ('runtime_error', 'Erro de Execução'), ('time_limit', 'Tempo Limite Excedido')], default='pending', max_length=20, verbose_name='Status')),
                ('result_message', models.TextField(blank=True, verbose_name='Mensagem de Resultado')),
                ('submitted_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Data de Submissão')),
                ('execution_time', models.FloatField(blank=True, null=True, verbose_name='Tempo de Execução (segundos)')),
                ('problem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='problems.problem', verbose_name='Desafio')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuário')),
            ],
            options={
                'verbose_name': 'Submissão',
                'verbose_name_plural': 'Submissões',
                'ordering': ['-submitted_at'],
            },
        ),
    ]

