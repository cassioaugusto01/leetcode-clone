# 🧪 Testes Unitários - CodePlatform

## 📋 Visão Geral

Suite completa de testes unitários para a plataforma LeetCode Clone.

## 📊 Cobertura de Testes

### ✅ test_models.py (4 classes, 20+ testes)
Testa todos os modelos da aplicação:
- **ProblemModelTest** - Modelo Problem (Desafio)
- **TestCaseModelTest** - Modelo TestCase (Casos de Teste)
- **SubmissionModelTest** - Modelo Submission (Submissões)
- **UserProfileModelTest** - Modelo UserProfile (Perfil)

### ✅ test_views.py (9 classes, 30+ testes)
Testa todas as views da aplicação:
- **HomeViewTest** - Página inicial
- **RegisterViewTest** - Registro de usuários
- **LoginViewTest** - Login
- **ProblemListViewTest** - Lista de desafios
- **ProblemDetailViewTest** - Detalhes do desafio
- **RunCodeViewTest** - Executar testes
- **SubmitCodeViewTest** - Submeter código
- **UserProfileViewTest** - Perfil do usuário

### ✅ test_code_executor.py (1 classe, 18+ testes)
Testa o executor de código Python:
- Execução bem-sucedida
- Respostas erradas
- Erros de sintaxe
- Erros em tempo de execução
- Função não encontrada
- Múltiplos casos de teste
- Diferentes tipos de entrada (list, dict, string)
- Medição de tempo
- Erros de JSON

### ✅ test_forms.py (2 classes, 15+ testes)
Testa os formulários:
- **UserRegistrationFormTest** - Formulário de registro
- **CodeSubmissionFormTest** - Formulário de código

## 🚀 Como Executar os Testes

### Executar Todos os Testes
```bash
python manage.py test
```

### Executar Testes de um App Específico
```bash
python manage.py test problems
```

### Executar Testes de um Módulo Específico
```bash
# Testes de modelos
python manage.py test problems.tests.test_models

# Testes de views
python manage.py test problems.tests.test_views

# Testes do executor
python manage.py test problems.tests.test_code_executor

# Testes de formulários
python manage.py test problems.tests.test_forms
```

### Executar um Teste Específico
```bash
python manage.py test problems.tests.test_models.ProblemModelTest.test_problem_creation
```

### Com Verbosidade
```bash
# Verbosidade nível 2 (detalhado)
python manage.py test --verbosity=2

# Verbosidade nível 3 (muito detalhado)
python manage.py test --verbosity=3
```

### Com Cobertura (Se tiver coverage instalado)
```bash
coverage run --source='.' manage.py test
coverage report
coverage html  # Gera relatório HTML
```

### Manter Banco de Dados de Teste
```bash
python manage.py test --keepdb
```

## 📈 Estatísticas dos Testes

- **Total de arquivos de teste**: 4
- **Total de classes de teste**: 16
- **Total de testes**: 80+
- **Cobertura estimada**: ~85%

## 🎯 O Que é Testado

### Modelos
✅ Criação de objetos  
✅ Métodos personalizados  
✅ Relacionamentos (ForeignKey, OneToOne)  
✅ Verbose names  
✅ Signals (criação de UserProfile)  
✅ Validações  

### Views
✅ Status codes (200, 302, 404)  
✅ Templates corretos  
✅ Contexto das views  
✅ Autenticação requerida  
✅ Permissões  
✅ Filtros e buscas  
✅ Criação de objetos  
✅ Atualizações de dados  

### Executor de Código
✅ Execução bem-sucedida  
✅ Detecção de erros  
✅ Validação de resultados  
✅ Múltiplos tipos de entrada  
✅ Tratamento de exceções  
✅ Medição de performance  

### Formulários
✅ Validação de dados  
✅ Campos obrigatórios  
✅ Formatação  
✅ Widgets e atributos  
✅ Mensagens de erro  

## 🐛 Exemplo de Output

```bash
$ python manage.py test

Creating test database for alias 'default'...
System check identified no issues (0 silenced).
................................................................................
----------------------------------------------------------------------
Ran 80 tests in 5.234s

OK
Destroying test database for alias 'default'...
```

## 📝 Boas Práticas Utilizadas

1. ✅ **Isolamento**: Cada teste é independente
2. ✅ **setUp**: Configuração inicial em cada classe
3. ✅ **Nomenclatura clara**: test_<what>_<condition>
4. ✅ **Asserções específicas**: assertEqual, assertTrue, assertIn
5. ✅ **Coverage completa**: Testa sucesso e falha
6. ✅ **Dados de teste**: Usa fixtures temporários
7. ✅ **Documentação**: Docstrings em todos os testes

## 🔄 Integração Contínua

Para CI/CD, adicione ao seu workflow:

```yaml
# .github/workflows/tests.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.9
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      - name: Run tests
        run: |
          python manage.py test
```

## 🎓 Adicionar Novos Testes

### Template de Teste
```python
from django.test import TestCase

class MyNewTest(TestCase):
    """Descrição do que está sendo testado"""
    
    def setUp(self):
        """Configuração executada antes de cada teste"""
        # Criar objetos necessários
        pass
    
    def test_something_works(self):
        """Testa se algo funciona como esperado"""
        # Arrange (preparar)
        # Act (executar)
        # Assert (verificar)
        self.assertEqual(expected, actual)
    
    def test_something_fails(self):
        """Testa se algo falha quando deve"""
        # Testar cenários de falha
        pass
```

## 📊 Relatório de Cobertura

### Instalar Coverage
```bash
pip install coverage
```

### Gerar Relatório
```bash
coverage run --source='.' manage.py test
coverage report -m
coverage html
```

Abra `htmlcov/index.html` no navegador.

## 🎯 Próximos Testes a Adicionar

- [ ] Testes de integração
- [ ] Testes de API (se adicionar)
- [ ] Testes de performance
- [ ] Testes de segurança
- [ ] Testes de acessibilidade
- [ ] Testes E2E com Selenium

## 💡 Dicas

1. Execute testes antes de commit
2. Mantenha testes rápidos
3. Use `--keepdb` para acelerar
4. Teste casos extremos (edge cases)
5. Documente comportamentos esperados

---

**✅ Suite de testes completa e funcional!**

