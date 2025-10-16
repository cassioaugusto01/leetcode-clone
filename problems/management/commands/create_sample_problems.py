from django.core.management.base import BaseCommand
from problems.models import Challenge, TestCase
import json


class Command(BaseCommand):
    help = 'Cria desafios de exemplo para a plataforma'

    def handle(self, *args, **kwargs):
        self.stdout.write('Criando desafios de exemplo...')
        
        # Desafio 1: Soma de Dois Números
        challenge1, created = Challenge.objects.get_or_create(
            slug='soma-de-dois-numeros',
            defaults={
                'title': 'Soma de Dois Números',
                'description': '''Dado dois números inteiros, retorne a soma deles.

Escreva uma função que recebe dois parâmetros (a e b) e retorna a + b.''',
                'difficulty': 'easy',
                'starter_code': '''def solution(a, b):
    # Escreva seu código aqui
    pass''',
                'function_name': 'solution'
            }
        )
        
        if created:
            TestCase.objects.create(
                challenge=challenge1,
                input_data=json.dumps([2, 3]),
                expected_output=json.dumps(5),
                is_sample=True,
                description='2 + 3 = 5'
            )
            TestCase.objects.create(
                problem=problem1,
                input_data=json.dumps([10, 20]),
                expected_output=json.dumps(30),
                is_sample=True,
                description='10 + 20 = 30'
            )
            TestCase.objects.create(
                problem=problem1,
                input_data=json.dumps([-5, 5]),
                expected_output=json.dumps(0),
                is_sample=False
            )
            TestCase.objects.create(
                problem=problem1,
                input_data=json.dumps([100, 200]),
                expected_output=json.dumps(300),
                is_sample=False
            )
            self.stdout.write(self.style.SUCCESS('✓ Desafio "Soma de Dois Números" criado'))
        
        # Desafio 2: Número Par ou Ímpar
        challenge2, created = Challenge.objects.get_or_create(
            slug='numero-par-ou-impar',
            defaults={
                'title': 'Número Par ou Ímpar',
                'description': '''Dado um número inteiro, retorne True se ele for par, e False se for ímpar.

Um número é par se for divisível por 2 (resto da divisão por 2 igual a 0).''',
                'difficulty': 'easy',
                'starter_code': '''def solution(n):
    # Escreva seu código aqui
    # Retorne True se n for par, False se for ímpar
    pass''',
                'function_name': 'solution'
            }
        )
        
        if created:
            TestCase.objects.create(
                challenge=challenge2,
                input_data=json.dumps([4]),
                expected_output=json.dumps(True),
                is_sample=True,
                description='4 é par'
            )
            TestCase.objects.create(
                challenge=challenge2,
                input_data=json.dumps([7]),
                expected_output=json.dumps(False),
                is_sample=True,
                description='7 é ímpar'
            )
            TestCase.objects.create(
                challenge=challenge2,
                input_data=json.dumps([0]),
                expected_output=json.dumps(True),
                is_sample=False
            )
            TestCase.objects.create(
                challenge=challenge2,
                input_data=json.dumps([100]),
                expected_output=json.dumps(True),
                is_sample=False
            )
            TestCase.objects.create(
                challenge=challenge2,
                input_data=json.dumps([101]),
                expected_output=json.dumps(False),
                is_sample=False
            )
            self.stdout.write(self.style.SUCCESS('✓ Desafio "Número Par ou Ímpar" criado'))
        
        # Desafio 3: Inverter String
        challenge3, created = Challenge.objects.get_or_create(
            slug='inverter-string',
            defaults={
                'title': 'Inverter String',
                'description': '''Dado uma string, retorne ela invertida.

Por exemplo, se a entrada for "hello", a saída deve ser "olleh".''',
                'difficulty': 'easy',
                'starter_code': '''def solution(s):
    # Escreva seu código aqui
    # Retorne a string s invertida
    pass''',
                'function_name': 'solution'
            }
        )
        
        if created:
            TestCase.objects.create(
                challenge=challenge3,
                input_data=json.dumps(["hello"]),
                expected_output=json.dumps("olleh"),
                is_sample=True,
                description='Inverter "hello"'
            )
            TestCase.objects.create(
                challenge=challenge3,
                input_data=json.dumps(["python"]),
                expected_output=json.dumps("nohtyp"),
                is_sample=True,
                description='Inverter "python"'
            )
            TestCase.objects.create(
                challenge=challenge3,
                input_data=json.dumps(["a"]),
                expected_output=json.dumps("a"),
                is_sample=False
            )
            TestCase.objects.create(
                challenge=challenge3,
                input_data=json.dumps([""]),
                expected_output=json.dumps(""),
                is_sample=False
            )
            self.stdout.write(self.style.SUCCESS('✓ Desafio "Inverter String" criado'))
        
        # Desafio 4: Fatorial
        challenge4, created = Challenge.objects.get_or_create(
            slug='fatorial',
            defaults={
                'title': 'Calcular Fatorial',
                'description': '''Calcule o fatorial de um número inteiro não-negativo n.

O fatorial de n (n!) é o produto de todos os inteiros positivos menores ou iguais a n.
Por exemplo: 5! = 5 × 4 × 3 × 2 × 1 = 120

Considere que 0! = 1''',
                'difficulty': 'medium',
                'starter_code': '''def solution(n):
    # Escreva seu código aqui
    # Retorne o fatorial de n
    pass''',
                'function_name': 'solution'
            }
        )
        
        if created:
            TestCase.objects.create(
                challenge=challenge4,
                input_data=json.dumps([5]),
                expected_output=json.dumps(120),
                is_sample=True,
                description='5! = 120'
            )
            TestCase.objects.create(
                challenge=challenge4,
                input_data=json.dumps([0]),
                expected_output=json.dumps(1),
                is_sample=True,
                description='0! = 1'
            )
            TestCase.objects.create(
                challenge=challenge4,
                input_data=json.dumps([1]),
                expected_output=json.dumps(1),
                is_sample=False
            )
            TestCase.objects.create(
                challenge=challenge4,
                input_data=json.dumps([10]),
                expected_output=json.dumps(3628800),
                is_sample=False
            )
            self.stdout.write(self.style.SUCCESS('✓ Desafio "Calcular Fatorial" criado'))
        
        # Desafio 5: Palíndromo
        challenge5, created = Challenge.objects.get_or_create(
            slug='palindromo',
            defaults={
                'title': 'Verificar Palíndromo',
                'description': '''Determine se uma string é um palíndromo.

Um palíndromo é uma palavra, frase ou sequência que pode ser lida da mesma forma de trás para frente.
Por exemplo: "arara", "radar", "ovo" são palíndromos.

Ignore espaços e considere apenas letras minúsculas.''',
                'difficulty': 'medium',
                'starter_code': '''def solution(s):
    # Escreva seu código aqui
    # Retorne True se s for um palíndromo, False caso contrário
    pass''',
                'function_name': 'solution'
            }
        )
        
        if created:
            TestCase.objects.create(
                challenge=challenge5,
                input_data=json.dumps(["arara"]),
                expected_output=json.dumps(True),
                is_sample=True,
                description='"arara" é palíndromo'
            )
            TestCase.objects.create(
                challenge=challenge5,
                input_data=json.dumps(["hello"]),
                expected_output=json.dumps(False),
                is_sample=True,
                description='"hello" não é palíndromo'
            )
            TestCase.objects.create(
                challenge=challenge5,
                input_data=json.dumps(["a"]),
                expected_output=json.dumps(True),
                is_sample=False
            )
            TestCase.objects.create(
                challenge=challenge5,
                input_data=json.dumps(["ovo"]),
                expected_output=json.dumps(True),
                is_sample=False
            )
            self.stdout.write(self.style.SUCCESS('✓ Desafio "Verificar Palíndromo" criado'))
        
        # Desafio 6: Fibonacci
        challenge6, created = Challenge.objects.get_or_create(
            slug='fibonacci',
            defaults={
                'title': 'Número de Fibonacci',
                'description': '''Retorne o n-ésimo número da sequência de Fibonacci.

A sequência de Fibonacci é: 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, ...
Onde cada número é a soma dos dois anteriores.

F(0) = 0, F(1) = 1, F(n) = F(n-1) + F(n-2) para n > 1''',
                'difficulty': 'medium',
                'starter_code': '''def solution(n):
    # Escreva seu código aqui
    # Retorne o n-ésimo número de Fibonacci
    pass''',
                'function_name': 'solution'
            }
        )
        
        if created:
            TestCase.objects.create(
                challenge=challenge6,
                input_data=json.dumps([0]),
                expected_output=json.dumps(0),
                is_sample=True,
                description='F(0) = 0'
            )
            TestCase.objects.create(
                challenge=challenge6,
                input_data=json.dumps([5]),
                expected_output=json.dumps(5),
                is_sample=True,
                description='F(5) = 5'
            )
            TestCase.objects.create(
                challenge=challenge6,
                input_data=json.dumps([10]),
                expected_output=json.dumps(55),
                is_sample=False
            )
            TestCase.objects.create(
                challenge=challenge6,
                input_data=json.dumps([15]),
                expected_output=json.dumps(610),
                is_sample=False
            )
            self.stdout.write(self.style.SUCCESS('✓ Desafio "Número de Fibonacci" criado'))
        
        # Desafio 7: Maior Elemento
        challenge7, created = Challenge.objects.get_or_create(
            slug='maior-elemento-lista',
            defaults={
                'title': 'Maior Elemento em uma Lista',
                'description': '''Dado uma lista de números inteiros, retorne o maior elemento.

Por exemplo, para [3, 7, 2, 9, 1], o maior elemento é 9.''',
                'difficulty': 'easy',
                'starter_code': '''def solution(nums):
    # Escreva seu código aqui
    # Retorne o maior elemento da lista nums
    pass''',
                'function_name': 'solution'
            }
        )
        
        if created:
            TestCase.objects.create(
                challenge=challenge7,
                input_data=json.dumps([[3, 7, 2, 9, 1]]),
                expected_output=json.dumps(9),
                is_sample=True,
                description='Maior elemento de [3, 7, 2, 9, 1] é 9'
            )
            TestCase.objects.create(
                challenge=challenge7,
                input_data=json.dumps([[1, 2, 3, 4, 5]]),
                expected_output=json.dumps(5),
                is_sample=True,
                description='Maior elemento de [1, 2, 3, 4, 5] é 5'
            )
            TestCase.objects.create(
                challenge=challenge7,
                input_data=json.dumps([[10]]),
                expected_output=json.dumps(10),
                is_sample=False
            )
            TestCase.objects.create(
                challenge=challenge7,
                input_data=json.dumps([[-5, -2, -10, -1]]),
                expected_output=json.dumps(-1),
                is_sample=False
            )
            self.stdout.write(self.style.SUCCESS('✓ Desafio "Maior Elemento em uma Lista" criado'))
        
        # Desafio 8: Ordenar Lista (Hard)
        challenge8, created = Challenge.objects.get_or_create(
            slug='ordenar-lista-sem-sort',
            defaults={
                'title': 'Ordenar Lista (Sem usar sort)',
                'description': '''Implemente uma função que ordena uma lista de números inteiros em ordem crescente.

IMPORTANTE: Você NÃO pode usar a função sort() ou sorted(). Implemente seu próprio algoritmo de ordenação.

Você pode usar algoritmos como Bubble Sort, Insertion Sort, Selection Sort, etc.''',
                'difficulty': 'hard',
                'starter_code': '''def solution(nums):
    # Escreva seu código aqui
    # Retorne a lista nums ordenada em ordem crescente
    # NÃO use sort() ou sorted()
    pass''',
                'function_name': 'solution'
            }
        )
        
        if created:
            TestCase.objects.create(
                challenge=challenge8,
                input_data=json.dumps([[5, 2, 8, 1, 9]]),
                expected_output=json.dumps([1, 2, 5, 8, 9]),
                is_sample=True,
                description='Ordenar [5, 2, 8, 1, 9]'
            )
            TestCase.objects.create(
                challenge=challenge8,
                input_data=json.dumps([[3, 3, 1, 2, 1]]),
                expected_output=json.dumps([1, 1, 2, 3, 3]),
                is_sample=True,
                description='Ordenar [3, 3, 1, 2, 1]'
            )
            TestCase.objects.create(
                challenge=challenge8,
                input_data=json.dumps([[1]]),
                expected_output=json.dumps([1]),
                is_sample=False
            )
            TestCase.objects.create(
                challenge=challenge8,
                input_data=json.dumps([[-5, 10, -3, 0, 7]]),
                expected_output=json.dumps([-5, -3, 0, 7, 10]),
                is_sample=False
            )
            self.stdout.write(self.style.SUCCESS('✓ Desafio "Ordenar Lista (Sem usar sort)" criado'))
        
        self.stdout.write(self.style.SUCCESS('\n✅ Todos os desafios de exemplo foram criados com sucesso!'))
        self.stdout.write('Execute "python manage.py runserver" e acesse http://localhost:8000')

