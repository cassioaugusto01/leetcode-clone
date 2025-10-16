# Guia de Uso - CodePlatform

## 📋 Índice
1. [Instalação](#instalação)
2. [Configuração Inicial](#configuração-inicial)
3. [Executando o Projeto](#executando-o-projeto)
4. [Usando a Plataforma](#usando-a-plataforma)
5. [Área Administrativa](#área-administrativa)
6. [Criando Novos Problemas](#criando-novos-problemas)

## 🚀 Instalação

### Método 1: Script Automático (Recomendado)

```bash
chmod +x setup.sh
./setup.sh
```

### Método 2: Instalação Manual

```bash
# 1. Criar ambiente virtual
python3 -m venv venv

# 2. Ativar ambiente virtual
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Aplicar migrações
python manage.py makemigrations
python manage.py migrate

# 5. Criar problemas de exemplo
python manage.py create_sample_problems

# 6. Criar superusuário
python manage.py createsuperuser
```

## ⚙️ Configuração Inicial

Após executar o setup, você terá:
- ✅ Banco de dados SQLite configurado
- ✅ 8 problemas de exemplo criados
- ✅ Sistema de autenticação configurado
- ✅ Área administrativa pronta

## 🏃 Executando o Projeto

```bash
# Ativar ambiente virtual (se não estiver ativo)
source venv/bin/activate

# Iniciar servidor
python manage.py runserver
```

Acesse: **http://localhost:8000**

## 📚 Usando a Plataforma

### Como Usuário

1. **Registrar-se**
   - Acesse http://localhost:8000/register/
   - Preencha o formulário de registro
   - Faça login automaticamente

2. **Navegar pelos Problemas**
   - Clique em "Problemas" no menu
   - Filtre por dificuldade ou pesquise por palavra-chave
   - Problemas resolvidos aparecem com ✓ verde

3. **Resolver um Problema**
   - Clique em um problema
   - Leia a descrição e exemplos
   - Escreva seu código no editor
   - Clique em "Executar Testes" para testar com exemplos
   - Clique em "Submeter" para avaliação completa

4. **Ver Seu Progresso**
   - Clique em seu nome de usuário no menu
   - Veja estatísticas, problemas resolvidos e histórico

### Exemplo de Solução

Para o problema "Soma de Dois Números":

```python
def solution(a, b):
    return a + b
```

## 🔧 Área Administrativa

### Acessar o Admin

URL: **http://localhost:8000/admin**

Use as credenciais do superusuário criado no setup.

### O que você pode fazer no Admin

- ✅ Criar, editar e deletar problemas
- ✅ Adicionar casos de teste
- ✅ Visualizar submissões dos usuários
- ✅ Gerenciar usuários
- ✅ Ver estatísticas da plataforma

## ➕ Criando Novos Problemas

### Via Admin Interface

1. Acesse http://localhost:8000/admin
2. Clique em "Problemas" → "Adicionar Problema"
3. Preencha os campos:

   **Informações Básicas:**
   - **Título**: Nome do problema
   - **Slug**: URL amigável (ex: soma-de-numeros)
   - **Descrição**: Explicação detalhada do problema
   - **Dificuldade**: Fácil, Médio ou Difícil

   **Configuração de Código:**
   - **Código Inicial**: Template que aparece no editor
   - **Nome da Função**: Nome da função que será testada (ex: solution)

4. **Adicionar Casos de Teste** (na mesma página):
   
   Para cada caso de teste:
   - **Entrada (JSON)**: Argumentos da função em formato JSON
   - **Saída Esperada (JSON)**: Resultado esperado em JSON
   - **Caso de Teste de Exemplo**: Marque se deve ser visível para os usuários
   - **Descrição**: Explicação opcional

### Exemplo Completo de Problema

**Título:** Somar Elementos de uma Lista

**Descrição:**
```
Dado uma lista de números inteiros, retorne a soma de todos os elementos.

Exemplo:
- Entrada: [1, 2, 3, 4, 5]
- Saída: 15
```

**Código Inicial:**
```python
def solution(nums):
    # Escreva seu código aqui
    pass
```

**Casos de Teste:**

| Entrada (JSON) | Saída (JSON) | É Exemplo? |
|----------------|--------------|------------|
| `[[1, 2, 3]]` | `6` | ✓ Sim |
| `[[10, 20, 30]]` | `60` | ✓ Sim |
| `[[]]` | `0` | ✗ Não |
| `[[-1, -2, -3]]` | `-6` | ✗ Não |

### Formato dos Dados de Teste

Os dados de entrada e saída devem estar em **formato JSON**:

**Para função com um parâmetro:**
```json
Entrada: [5]
Saída: 25
```

**Para função com múltiplos parâmetros:**
```json
Entrada: [10, 20]
Saída: 30
```

**Para função com lista:**
```json
Entrada: [[1, 2, 3, 4]]
Saída: 10
```

**Para função com strings:**
```json
Entrada: ["hello"]
Saída: "olleh"
```

## 🔒 Segurança do Código

O executor de código implementa várias medidas de segurança:

- ⏱️ **Timeout de 5 segundos** por execução
- 🔒 **Namespace isolado** para cada execução
- 🚫 **Sem acesso a arquivos ou rede**
- ✅ **Captura de erros e exceções**

**Nota:** Para produção, recomenda-se usar containers Docker para isolamento adicional.

## 📊 Problemas de Exemplo Incluídos

A plataforma vem com 8 problemas de exemplo:

1. **Soma de Dois Números** (Fácil)
2. **Número Par ou Ímpar** (Fácil)
3. **Inverter String** (Fácil)
4. **Maior Elemento em uma Lista** (Fácil)
5. **Calcular Fatorial** (Médio)
6. **Verificar Palíndromo** (Médio)
7. **Número de Fibonacci** (Médio)
8. **Ordenar Lista sem usar sort** (Difícil)

## 🛠️ Comandos Úteis

```bash
# Criar novo superusuário
python manage.py createsuperuser

# Aplicar migrações
python manage.py migrate

# Criar problemas de exemplo novamente
python manage.py create_sample_problems

# Acessar shell do Django
python manage.py shell

# Limpar banco de dados (cuidado!)
python manage.py flush
```

## 🐛 Solução de Problemas

### Erro: "No module named 'django'"
```bash
# Certifique-se de que o ambiente virtual está ativo
source venv/bin/activate
pip install -r requirements.txt
```

### Erro: "Table doesn't exist"
```bash
# Execute as migrações
python manage.py makemigrations
python manage.py migrate
```

### Erro ao submeter código
- Verifique se está logado
- Certifique-se de que há casos de teste cadastrados
- Verifique se o nome da função está correto

## 📝 Estrutura de Arquivos

```
leetcode-clone/
├── codingplatform/        # Configurações do Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── problems/              # App principal
│   ├── models.py         # Modelos de dados
│   ├── views.py          # Lógica das views
│   ├── forms.py          # Formulários
│   ├── admin.py          # Configuração do admin
│   ├── code_executor.py  # Executor de código
│   └── management/       # Comandos personalizados
├── templates/            # Templates HTML
│   ├── base.html
│   └── problems/
├── requirements.txt      # Dependências Python
├── manage.py            # CLI do Django
└── README.md            # Documentação
```

## 🎯 Próximos Passos

Sugestões para expandir a plataforma:

- [ ] Adicionar ranking de usuários
- [ ] Implementar sistema de tags para problemas
- [ ] Adicionar discussões nos problemas
- [ ] Suporte para múltiplas linguagens de programação
- [ ] Sistema de dicas progressivas
- [ ] Testes de performance (tempo e memória)
- [ ] API REST para integração
- [ ] Editor de código com syntax highlighting

## 📧 Suporte

Para problemas ou dúvidas:
1. Verifique a seção de Solução de Problemas
2. Revise os logs no terminal
3. Consulte a documentação do Django

---

**Bons estudos e boa codificação! 🚀**

