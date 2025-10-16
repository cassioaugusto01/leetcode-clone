# 🏗️ Arquitetura da Plataforma CodePlatform

## Visão Geral

A plataforma foi construída seguindo a arquitetura MVT (Model-View-Template) do Django, com separação clara de responsabilidades e organização modular.

## 📊 Diagrama de Arquitetura

```
┌─────────────────────────────────────────────────────────┐
│                    FRONTEND (Templates)                  │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌─────────┐ │
│  │  Home    │  │ Problems │  │  Solve   │  │ Profile │ │
│  └──────────┘  └──────────┘  └──────────┘  └─────────┘ │
└───────────────────────┬─────────────────────────────────┘
                        │ HTTP Requests
                        ▼
┌─────────────────────────────────────────────────────────┐
│                    DJANGO VIEWS                          │
│  ┌──────────────────────────────────────────────────┐   │
│  │  Authentication  │  Problem List  │  Code Submit │   │
│  └──────────────────────────────────────────────────┘   │
└───────────┬────────────────────────┬────────────────────┘
            │                        │
            ▼                        ▼
┌──────────────────────┐   ┌──────────────────────┐
│   BUSINESS LOGIC     │   │   CODE EXECUTOR      │
│  ┌────────────────┐  │   │  ┌────────────────┐  │
│  │ Validation     │  │   │  │ Isolated Env   │  │
│  │ Authorization  │  │   │  │ Timeout Handler│  │
│  │ Statistics     │  │   │  │ Test Runner    │  │
│  └────────────────┘  │   │  └────────────────┘  │
└──────────┬───────────┘   └──────────────────────┘
           │
           ▼
┌─────────────────────────────────────────────────────────┐
│                    DATABASE (SQLite)                     │
│  ┌────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │  User  │  │ Problem  │  │TestCase  │  │Submission│  │
│  └────────┘  └──────────┘  └──────────┘  └──────────┘  │
└─────────────────────────────────────────────────────────┘
```

## 🗂️ Estrutura de Arquivos Detalhada

### 1. Configuração do Projeto (`codingplatform/`)

```
codingplatform/
├── __init__.py          # Pacote Python
├── settings.py          # Configurações do Django
├── urls.py              # Roteamento principal
├── wsgi.py              # Interface WSGI
└── asgi.py              # Interface ASGI
```

**settings.py** contém:
- Configurações de banco de dados
- Apps instalados
- Middleware
- Configurações de templates
- Internacionalização (pt-BR)
- Arquivos estáticos

### 2. App Principal (`problems/`)

```
problems/
├── __init__.py          # Pacote Python
├── models.py            # Modelos de dados (4 modelos)
├── views.py             # Lógica das views (10 views)
├── urls.py              # Roteamento do app (10 URLs)
├── forms.py             # Formulários (2 forms)
├── admin.py             # Interface admin (4 admins)
├── apps.py              # Configuração do app
├── signals.py           # Signals para UserProfile
├── code_executor.py     # Executor de código Python
├── migrations/          # Migrações do banco
└── management/          # Comandos customizados
    └── commands/
        └── create_sample_problems.py
```

### 3. Templates (`templates/`)

```
templates/
├── base.html                    # Template base com navbar, footer, CSS
└── problems/
    ├── home.html                # Página inicial
    ├── login.html               # Login de usuário
    ├── register.html            # Registro de usuário
    ├── problem_list.html        # Lista de problemas
    ├── problem_detail.html      # Resolver problema
    ├── profile.html             # Perfil do usuário
    └── submission_detail.html   # Detalhes da submissão
```

## 📦 Modelos de Dados

### Problem (Problema)
```python
- id: AutoField (PK)
- title: CharField(200)
- slug: SlugField (unique)
- description: TextField
- difficulty: CharField (easy/medium/hard)
- created_at: DateTimeField
- updated_at: DateTimeField
- starter_code: TextField
- function_name: CharField(100)

Métodos:
- get_solved_count(): Retorna quantos usuários resolveram
```

### TestCase (Caso de Teste)
```python
- id: AutoField (PK)
- problem: ForeignKey(Problem)
- input_data: TextField (JSON)
- expected_output: TextField (JSON)
- is_sample: BooleanField
- description: CharField(200)
```

### Submission (Submissão)
```python
- id: AutoField (PK)
- user: ForeignKey(User)
- problem: ForeignKey(Problem)
- code: TextField
- status: CharField (pending/running/accepted/wrong_answer/runtime_error/time_limit)
- result_message: TextField
- submitted_at: DateTimeField
- execution_time: FloatField
```

### UserProfile (Perfil do Usuário)
```python
- id: AutoField (PK)
- user: OneToOneField(User)
- problems_solved: IntegerField
- total_submissions: IntegerField

Criado automaticamente via signal quando User é criado
```

## 🔄 Fluxo de Dados

### 1. Fluxo de Autenticação

```
1. User acessa /register/
2. Preenche formulário UserRegistrationForm
3. View register() valida dados
4. Cria User no banco
5. Signal cria UserProfile automaticamente
6. Login automático
7. Redirect para problem_list
```

### 2. Fluxo de Resolução de Problema

```
1. User acessa /problem/<slug>/
2. View problem_detail() carrega:
   - Problema
   - Casos de teste de exemplo
   - Submissões anteriores
3. User escreve código no editor
4. Clica "Executar Testes":
   ├─> AJAX POST para /problem/<slug>/run/
   ├─> View run_code() executa code_executor
   ├─> Retorna JSON com resultados
   └─> JavaScript atualiza interface

5. Clica "Submeter":
   ├─> AJAX POST para /problem/<slug>/submit/
   ├─> View submit_code() cria Submission
   ├─> Executa código com TODOS os casos de teste
   ├─> Atualiza status da Submission
   ├─> Atualiza UserProfile (se aceito)
   └─> Retorna JSON com resultado completo
```

### 3. Fluxo do Executor de Código

```python
# code_executor.py

1. execute_code(code, test_cases, function_name)
2. Cria namespace isolado: {}
3. Configura timeout de 5 segundos (signal.alarm)
4. Redireciona stdout (captura prints)
5. exec(code, namespace)  # Executa código do usuário
6. Para cada test_case:
   ├─> Parse JSON input
   ├─> Chama user_function(*args)
   ├─> Compara output com expected_output
   └─> Registra resultado (passed/failed)
7. Cancela timeout
8. Retorna dict com status, message, test_results, execution_time
```

## 🔒 Segurança

### Executor de Código

**Medidas Implementadas:**
1. **Timeout**: 5 segundos máximo (signal.SIGALRM)
2. **Namespace Isolado**: exec() em dict vazio
3. **Captura de Stdout**: Previne outputs indesejados
4. **Try-Except**: Captura todas as exceções
5. **Validação de JSON**: Parse seguro dos dados

**Limitações Atuais:**
- Ainda é possível usar imports
- Acesso a alguns recursos do sistema
- Não há limite de memória

**Recomendações para Produção:**
- Usar Docker containers
- Implementar cgroups para limitar CPU/memória
- Blacklist de imports perigosos
- Sandboxing adicional (firejail, nsjail)

### Autenticação

**Implementado:**
- Hashing de senhas (PBKDF2 SHA256)
- CSRF protection
- Login required decorators
- Session management

## 🌐 APIs e Endpoints

### Públicos (sem autenticação)
```
GET  /                      → home (página inicial)
GET  /problems/             → problem_list
GET  /problem/<slug>/       → problem_detail
GET  /register/             → register
GET  /login/                → user_login
GET  /logout/               → user_logout
```

### Requer Autenticação
```
POST /problem/<slug>/run/       → run_code (AJAX)
POST /problem/<slug>/submit/    → submit_code (AJAX)
GET  /profile/                  → user_profile
GET  /submission/<id>/          → submission_detail
```

### Admin
```
GET/POST /admin/*               → Django Admin Interface
```

## 🎨 Frontend

### Tecnologias
- **Bootstrap 5**: Framework CSS
- **Bootstrap Icons**: Ícones
- **Vanilla JavaScript**: Interatividade
- **AJAX/Fetch API**: Comunicação assíncrona

### Componentes Principais

**Base Template** (`base.html`):
- Navbar com links dinâmicos
- Sistema de mensagens (Django messages)
- Footer
- CSS customizado (gradientes, badges, cards)

**Editor de Código** (`problem_detail.html`):
- Textarea com monospace font
- Botões Run/Submit
- Área de resultados dinâmica
- JavaScript para AJAX requests

## 📊 Banco de Dados

### SQLite (Padrão)
- Arquivo: `db.sqlite3`
- Sem configuração adicional
- Ideal para desenvolvimento

### Migração para PostgreSQL (Opcional)

```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'codingplatform',
        'USER': 'postgres',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## 🔧 Customização e Extensão

### Adicionar Nova Linguagem

1. Criar novo executor (ex: `java_executor.py`)
2. Adicionar campo `language` em Problem
3. Adaptar views para escolher executor
4. Atualizar templates com seletor de linguagem

### Adicionar Rankings

1. Criar model `Ranking`
2. Adicionar view `leaderboard()`
3. Calcular pontos baseado em dificuldade
4. Criar template de ranking

### Adicionar Discussões

1. Criar model `Discussion`
2. Associar com Problem
3. Adicionar views de CRUD
4. Templates de fórum

## 📈 Performance

### Otimizações Implementadas
- `select_related()` para ForeignKeys
- `values_list()` para queries específicas
- Indexes em campos slug
- Query optimization em views

### Melhorias Futuras
- Cache de problemas frequentes (Redis)
- Async views para operações longas
- CDN para assets estáticos
- Database indexing adicional
- Query optimization com prefetch_related

## 🧪 Testing

### Estrutura de Testes Sugerida

```python
# problems/tests.py

class ProblemModelTest(TestCase):
    # Testar criação de problemas
    # Testar validações
    
class CodeExecutorTest(TestCase):
    # Testar execução correta
    # Testar timeout
    # Testar erros
    
class ViewsTest(TestCase):
    # Testar autenticação
    # Testar submissões
    # Testar edge cases
```

## 🚀 Deploy

### Checklist para Produção

- [ ] Mudar `DEBUG = False`
- [ ] Configurar `ALLOWED_HOSTS`
- [ ] Usar PostgreSQL
- [ ] Configurar `STATIC_ROOT` e `MEDIA_ROOT`
- [ ] Usar variáveis de ambiente (.env)
- [ ] Configurar HTTPS
- [ ] Adicionar logging
- [ ] Configurar email
- [ ] Backup do banco de dados
- [ ] Monitoring (Sentry)

### Plataformas Recomendadas
- **Heroku**: Fácil deploy
- **DigitalOcean**: VPS com Docker
- **AWS**: Escalável
- **PythonAnywhere**: Específico para Python

## 📚 Referências

- [Django Documentation](https://docs.djangoproject.com/)
- [Bootstrap Documentation](https://getbootstrap.com/)
- [Python exec() Security](https://docs.python.org/3/library/functions.html#exec)

---

**Arquitetura criada para ser modular, escalável e fácil de manter.**

