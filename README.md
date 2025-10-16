# 🚀 LeetCode Clone - Plataforma de Programação

Uma plataforma de programação completa similar ao LeetCode construída com Django e Python.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Django](https://img.shields.io/badge/Django-4.2-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📋 Recursos Implementados

✅ **1. Ambiente de Resolução de Desafios**
   - Editor de código integrado
   - Suporte para Python
   - Interface moderna e responsiva

✅ **2. Sistema de Testes Unitários**
   - Execução de testes de exemplo
   - Validação automática de soluções
   - Feedback detalhado de erros

✅ **3. Sistema de Submissão e Avaliação**
   - Submissão de soluções
   - Avaliação automática com todos os casos de teste
   - Registro de resultados por usuário
   - Histórico de submissões

✅ **4. Autenticação de Usuários**
   - Registro de novos usuários
   - Sistema de login/logout
   - Perfil de usuário com estatísticas
   - Controle de acesso

✅ **5. Área Administrativa**
   - Interface admin do Django customizada
   - Criação e edição de problemas
   - Gerenciamento de casos de teste
   - Visualização de submissões
   - Gerenciamento de usuários

## 🎯 Recursos Adicionais

- 📊 Dashboard com estatísticas
- 🏆 Rastreamento de progresso do usuário
- 🎨 Interface moderna com Bootstrap 5
- 🔍 Sistema de busca e filtros
- 📱 Design responsivo
- ⏱️ Medição de tempo de execução
- 🎯 8 desafios de exemplo incluídos
- 🔒 Execução segura de código com timeout

## 🚀 Início Rápido

### Método Automático (Recomendado)

```bash
# Clone o repositório (se aplicável)
cd leetcode-clone

# Execute o script de setup
chmod +x setup.sh
./setup.sh

# Ative o ambiente virtual
source venv/bin/activate

# Inicie o servidor
python manage.py runserver
```

### Método Manual

```bash
# 1. Criar ambiente virtual
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou venv\Scripts\activate no Windows

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Aplicar migrações
python manage.py makemigrations
python manage.py migrate

# 4. Criar desafios de exemplo
python manage.py create_sample_problems

# 5. Criar superusuário
python manage.py createsuperuser

# 6. Iniciar servidor
python manage.py runserver
```

🎉 **Pronto!** Acesse http://localhost:8000

## 📚 Documentação

- 📖 **[QUICK_START.md](QUICK_START.md)** - Guia rápido de 5 minutos
- 📖 **[GUIA_DE_USO.md](GUIA_DE_USO.md)** - Documentação completa
- 🔧 **Admin**: http://localhost:8000/admin
- 💻 **Plataforma**: http://localhost:8000

## 🏗️ Estrutura do Projeto

```
leetcode-clone/
├── codingplatform/              # Configurações Django
│   ├── settings.py             # Configurações principais
│   ├── urls.py                 # URLs do projeto
│   └── wsgi.py                 # WSGI config
├── problems/                    # App principal
│   ├── models.py               # Modelos (Problem, TestCase, Submission)
│   ├── views.py                # Views e lógica de negócio
│   ├── forms.py                # Formulários
│   ├── admin.py                # Configuração do admin
│   ├── code_executor.py        # Executor de código Python
│   ├── urls.py                 # URLs do app
│   ├── signals.py              # Signals (criação de perfil)
│   └── management/             # Comandos customizados
│       └── commands/
│           └── create_sample_problems.py
├── templates/                   # Templates HTML
│   ├── base.html               # Template base
│   └── problems/               # Templates específicos
│       ├── home.html           # Página inicial
│       ├── problem_list.html   # Lista de problemas
│       ├── problem_detail.html # Resolver problema
│       ├── profile.html        # Perfil do usuário
│       ├── login.html          # Login
│       ├── register.html       # Registro
│       └── submission_detail.html
├── static/                      # Arquivos estáticos (CSS, JS, imagens)
├── requirements.txt             # Dependências Python
├── manage.py                    # CLI do Django
├── setup.sh                     # Script de instalação
├── README.md                    # Este arquivo
├── QUICK_START.md              # Guia rápido
└── GUIA_DE_USO.md              # Documentação completa
```

## 💻 Tecnologias Utilizadas

- **Backend**: Django 4.2
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Banco de Dados**: SQLite (padrão) / PostgreSQL (opcional)
- **Executor de Código**: Python exec() com isolamento
- **Ícones**: Bootstrap Icons

## 🎓 Desafios Incluídos

A plataforma vem com **8 desafios de exemplo**:

### Fácil (4 desafios)
1. Soma de Dois Números
2. Número Par ou Ímpar
3. Inverter String
4. Maior Elemento em uma Lista

### Médio (3 desafios)
5. Calcular Fatorial
6. Verificar Palíndromo
7. Número de Fibonacci

### Difícil (1 desafio)
8. Ordenar Lista (sem usar sort)

## 🔧 Funcionalidades Principais

### Para Usuários
- ✅ Cadastro e login
- ✅ Navegação por desafios
- ✅ Filtrar por dificuldade
- ✅ Buscar desafios
- ✅ Escrever código no editor
- ✅ Executar testes de exemplo
- ✅ Submeter solução
- ✅ Ver histórico de submissões
- ✅ Acompanhar progresso

### Para Administradores
- ✅ Criar novos desafios
- ✅ Adicionar casos de teste
- ✅ Gerenciar usuários
- ✅ Visualizar submissões
- ✅ Ver estatísticas da plataforma

## 🛠️ Comandos Úteis

```bash
# Criar superusuário
python manage.py createsuperuser

# Criar desafios de exemplo
python manage.py create_sample_problems

# Aplicar migrações
python manage.py migrate

# Criar migrações
python manage.py makemigrations

# Shell interativo
python manage.py shell

# Executar testes
python manage.py test

# Coletar arquivos estáticos (produção)
python manage.py collectstatic
```

## 🔒 Segurança

O executor de código implementa várias camadas de segurança:

- ⏱️ **Timeout de 5 segundos** por execução
- 🔒 **Namespace isolado** para cada execução
- 🚫 **Sem acesso a arquivos ou rede** no ambiente de execução
- ✅ **Captura e tratamento de exceções**
- 🛡️ **Validação de entrada de dados**

⚠️ **Nota**: Para ambiente de produção, recomenda-se usar containers Docker para isolamento adicional.

## 📊 Modelo de Dados

```python
# Principais modelos

Problem         # Desafio
├── title       # Título
├── slug        # URL amigável
├── description # Descrição
├── difficulty  # Fácil/Médio/Difícil
└── test_cases  # Casos de teste

TestCase        # Caso de Teste
├── problem     # FK para Problem (Desafio)
├── input_data  # Entrada (JSON)
├── expected_output  # Saída esperada (JSON)
└── is_sample   # Se é exemplo visível

Submission      # Submissão de Solução
├── user        # FK para User
├── problem     # FK para Problem (Desafio)
├── code        # Código submetido
├── status      # accepted/wrong_answer/error/timeout
└── execution_time  # Tempo de execução

UserProfile     # Perfil do Usuário
├── user        # OneToOne para User
├── problems_solved     # Total de desafios resolvidos
└── total_submissions   # Total de submissões
```

## 🎨 Customização

### Cores e Estilos

Edite `templates/base.html` para personalizar:
- Cores do tema (variáveis CSS)
- Gradientes
- Estilos dos badges de dificuldade
- Layout geral

### Adicionar Novos Desafios

Via Admin:
1. Acesse http://localhost:8000/admin
2. Vá em Desafios → Adicionar Desafio
3. Preencha os campos
4. Adicione casos de teste
5. Salve

Via Código:
- Edite `problems/management/commands/create_sample_problems.py`
- Adicione novos desafios seguindo o padrão

## 🐛 Solução de Problemas

### Django não encontrado
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Erro de migração
```bash
python manage.py makemigrations
python manage.py migrate
```

### Porta 8000 em uso
```bash
python manage.py runserver 8001
```

### Problemas de permissão no Linux/Mac
```bash
chmod +x setup.sh
```

## 🚀 Próximas Funcionalidades (Sugestões)

- [ ] Ranking global de usuários
- [ ] Sistema de conquistas/badges
- [ ] Discussões nos problemas
- [ ] Suporte para JavaScript, C++, Java
- [ ] Editor com syntax highlighting
- [ ] Modo escuro
- [ ] Testes de performance (tempo/memória)
- [ ] API REST
- [ ] Contests/Competições
- [ ] Sistema de dicas

## 📝 Licença

Este projeto é de código aberto e está disponível para fins educacionais.

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para:
- Reportar bugs
- Sugerir novas funcionalidades
- Melhorar a documentação
- Adicionar novos desafios

## 📧 Contato e Suporte

Para dúvidas ou problemas:
1. Consulte a documentação em `GUIA_DE_USO.md`
2. Verifique a seção de solução de problemas
3. Revise os logs do terminal

---

**Desenvolvido com ❤️ usando Django e Python**

**Bons estudos e happy coding! 🚀💻**

